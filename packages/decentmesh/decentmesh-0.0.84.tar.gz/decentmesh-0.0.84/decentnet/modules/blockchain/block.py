import asyncio
import logging
import struct
import time
from typing import Union

from Crypto.Util.Padding import pad, unpad

from decentnet.consensus.block_sizing import MERGED_DIFFICULTY_BYTE_LEN, HASH_LEN, \
    INDEX_SIZE, NONCE_SIZE, TIMESTAMP_SIZE, HASH_LEN_BLOCK
from decentnet.consensus.byte_conversion_constants import ENDIAN_TYPE
from decentnet.consensus.dev_constants import RUN_IN_DEBUG, BLOCK_ERROR_DATA_LOG_LEN
from decentnet.modules.compression.wrapper import CompressionWrapper
from decentnet.modules.hash_type.hash_type import MemoryHash, ShaHash
from decentnet.modules.logger.log import setup_logger
from decentnet.modules.monitoring.metric_server import send_metric
from decentnet.modules.pow.difficulty import Difficulty
from decentnet.modules.pow.pow import PoW
from decentnet.modules.timer.timer import Timer

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


class Block:
    index: int
    previous_hash: bytes = None
    diff: Difficulty
    data: bytearray
    timestamp: float
    nonce: int | None
    _hash: MemoryHash | ShaHash | None
    ttc: float
    signature: str | None = None

    def __init__(self, index: int, prev_hash: bytes,
                 difficulty: Difficulty,
                 data: Union[bytearray, bytes], do_metric: bool = False):
        self.index = index
        self.previous_hash = prev_hash
        self.data = data
        self.diff = difficulty
        self.timestamp = time.time()
        self.nonce = 0
        self.signature = None
        self.do_metric = do_metric

        if not self.do_metric:
            logger.warning("Metrics in Block will not be collected.. FAIL")

    def __str__(self):
        dd = str(bytes(self.data))
        display_data = dd[:BLOCK_ERROR_DATA_LOG_LEN] + "..." if len(
            dd) > BLOCK_ERROR_DATA_LOG_LEN else dd
        result = f"Block #{self.index}\n" \
                 f"Previous Hash: {self.previous_hash.hex()[2:].zfill(HASH_LEN) if self.index != 0 else 'GENESIS BLOCK'}\n" \
                 f"Difficulty: {self.diff}\n" \
                 f"Data: {display_data}\n" \
                 f"Timestamp: {self.timestamp}\n" \
                 f"Nonce: {self.nonce}\n"

        if hasattr(self, "_hash"):
            result += f"Hash: {self.hash.value.hex()[2:].zfill(HASH_LEN)}\n"

        return result

    @property
    def hash(self):
        return self._hash

    def compute_hash(self) -> MemoryHash | ShaHash:
        index_bytes = self.index.to_bytes(INDEX_SIZE, byteorder=ENDIAN_TYPE, signed=False)
        diff_bytes = self.diff.to_bytes()
        previous_hash_bytes = self.previous_hash
        timestamp_bytes = struct.pack('d', self.timestamp)

        packed_block = (
                index_bytes + diff_bytes + previous_hash_bytes + timestamp_bytes + self.data)

        if not self.diff.express:
            self._hash = MemoryHash(self.diff, packed_block)
        else:
            self._hash = ShaHash(self.diff, packed_block)

        return self._hash

    def to_bytes(self) -> bytes:
        index_bytes = self.index.to_bytes(INDEX_SIZE, byteorder=ENDIAN_TYPE, signed=False)
        diff_bytes = self.diff.to_bytes()

        previous_hash_bytes = pad(bytes(self.previous_hash), HASH_LEN_BLOCK, style='pkcs7')

        nonce_bytes = self.nonce.to_bytes(NONCE_SIZE, byteorder=ENDIAN_TYPE,
                                          signed=False)
        timestamp_bytes = struct.pack('d', self.timestamp)

        compressed_data = self.data if self.diff.compression_level == 0 else CompressionWrapper.compress_lz4(
            self.data, self.diff.compression_level)

        packed_block = (index_bytes + diff_bytes + previous_hash_bytes +
                        nonce_bytes + timestamp_bytes + compressed_data)  # Speed up compression

        packed_block_len = len(packed_block)

        if self.do_metric:
            compressed_data_len = len(compressed_data)
            asyncio.run(send_metric("data_header_ratio", compressed_data_len / packed_block_len))
            logger.debug(
                f"Data ratio {compressed_data_len / packed_block_len} {compressed_data_len} {packed_block_len}")

        logger.debug(f"Packed Block into {packed_block_len} B")
        return packed_block

    @classmethod
    def from_bytes(cls, compressed_block_bytes: bytes):
        block = cls.__new__(cls)

        block_bytes = memoryview(compressed_block_bytes)

        cursor = 0

        # Unpack index
        block.index = int.from_bytes(block_bytes[cursor:cursor + INDEX_SIZE], byteorder=ENDIAN_TYPE,
                                     signed=False)
        cursor += INDEX_SIZE

        # Unpack difficulty
        block.diff = Difficulty.from_bytes(block_bytes[cursor:cursor + MERGED_DIFFICULTY_BYTE_LEN])
        cursor += MERGED_DIFFICULTY_BYTE_LEN

        # Unpack previous hash
        block.previous_hash = unpad(bytes(block_bytes[cursor:cursor + HASH_LEN_BLOCK]), HASH_LEN_BLOCK,
                                    style='pkcs7')
        cursor += HASH_LEN_BLOCK

        # Unpack nonce
        block.nonce = int.from_bytes(block_bytes[cursor:cursor + NONCE_SIZE],
                                     byteorder=ENDIAN_TYPE,
                                     signed=False)
        cursor += NONCE_SIZE

        # Unpack timestamp
        block.timestamp = struct.unpack("d", block_bytes[cursor:cursor + TIMESTAMP_SIZE])[0]
        cursor += TIMESTAMP_SIZE

        # Decompress the remaining data
        block.data = block_bytes[
                     cursor:] if block.diff.compression_level == 0 else CompressionWrapper.decompress_lz4(
            block_bytes[cursor:])

        return block

    def mine(self, measure=False):
        logger.debug(f"Mining block #{self.index}")
        if measure:
            t = Timer()

        a = self.compute_hash()

        finished_hash, finished_nonce = PoW.compute(a, self.diff.n_bits, express=self.diff.express)
        self.nonce = finished_nonce

        if measure:
            self.ttc = t.stop()
            return finished_nonce, self.ttc
        else:
            return finished_nonce
