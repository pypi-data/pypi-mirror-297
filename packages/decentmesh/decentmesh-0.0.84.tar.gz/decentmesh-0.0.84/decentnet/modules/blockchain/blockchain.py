import asyncio
import logging
from collections import deque

import cbor2

from decentnet.__version__ import NETWORK_VERSION
from decentnet.consensus.blockchain_params import BlockchainParams, SAVE_BLOCKS_TO_DB_DEFAULT
from decentnet.consensus.cmd_enum import CMD
from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.modules.blockchain.block import Block
from decentnet.modules.convert.byte_to_base64_utils import bytes_to_base64
from decentnet.modules.cryptography.asymetric import AsymCrypt
from decentnet.modules.db.base import session_scope
from decentnet.modules.db.models import BlockchainTable, BlockTable, BlockSignatureTable
from decentnet.modules.key_util.key_manager import KeyManager
from decentnet.modules.logger.log import setup_logger
from decentnet.modules.monitoring.metric_server import send_metric
from decentnet.modules.passgen.passgen import SecurePasswordGenerator
from decentnet.modules.pow.difficulty import Difficulty
from decentnet.modules.pow.pow_utils import PowUtils
from decentnet.modules.timer.timer import Timer

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


class Blockchain:
    _id: int
    chain: deque[Block]
    version: bytes
    _difficulty: Difficulty

    def __init__(self, genesis_data: str | None = None, save=SAVE_BLOCKS_TO_DB_DEFAULT,
                 difficulty: Difficulty = BlockchainParams.seed_difficulty,
                 pub_key_for_encryption: str | None = None,
                 beam_id: int | None = None,
                 next_difficulty: Difficulty = BlockchainParams.low_diff_sha256, name="default",
                 do_metric: bool = False):
        self.version = NETWORK_VERSION
        self.pub_key_for_encryption = pub_key_for_encryption
        self._difficulty = difficulty
        self.chain: deque[Block] = deque()
        self.save = save
        self.name = name
        self._id = -1
        self.do_metric = do_metric

        if not self.do_metric:
            logger.warning("Metrics in Blockchain will not be collected.. FAIL")

        if save:
            asyncio.run(self.__save(beam_id))

        if genesis_data:
            if self.pub_key_for_encryption is None:
                logger.warning(
                    "Public key for encryption not provided, data will be not encrypted.")

            seed_block = self.create_genesis(genesis_data.encode("ascii"),
                                             owned_public_key_for_encryption=self.pub_key_for_encryption,
                                             difficulty=difficulty,
                                             next_difficulty=next_difficulty, do_metric=do_metric)
            seed_block.mine()
            if not self.insert(seed_block):
                raise Exception("Failed to insert genesis block")

            self.difficulty = next_difficulty

    async def __save(self, beam_id):
        async with session_scope() as session:
            b_gen = BlockchainTable(
                version=self.version.hex(),
                beam_id=beam_id,
                difficulty=str(self.difficulty)
            )
            session.add(b_gen)
            await session.commit()
            self._id = b_gen.blockchain_id

    def __len__(self):
        return len(self.chain)

    @classmethod
    def create_genesis(cls, data, owned_public_key_for_encryption: str | None,
                       difficulty: Difficulty = BlockchainParams.seed_difficulty,
                       next_difficulty: Difficulty = BlockchainParams.low_diff_sha256,
                       do_metric: bool = False):

        genesis_data = cbor2.dumps({"data": data.decode("ascii"),
                                    "new_diff": next_difficulty.to_bytes().decode("ascii"),
                                    "enc_pub_key": owned_public_key_for_encryption})
        block = Block(0, b"0", difficulty, genesis_data, do_metric)
        block.seed_hash = block.compute_hash()
        return block

    @classmethod
    def convert_handshake_block_dict_to_bytes(cls, handshake_block: dict) -> bytes:
        return cbor2.dumps(handshake_block)

    @classmethod
    def create_handshake_encryption_block_raw(cls,
                                              public_key_received_for_encryption: str,
                                              bits: int = 192, algorithm: str = "AES",
                                              additional_data: str = "") -> (bytes, bytes):
        """
        Create handshake encryption data for block
        :param additional_data:
        :param public_key_received_for_encryption:
        :param bits:
        :param algorithm:
        :return: handshake block in raw byte format dumped by cbor2, password
        """
        logger.debug(f"Creating handshake block with pub_enc {public_key_received_for_encryption}")
        encrypted_password, password = cls._create_handshake_block_base(bits,
                                                                        public_key_received_for_encryption)

        data = cls.convert_handshake_block_dict_to_bytes(
            {"cmd": CMD.HANDSHAKE_ENCRYPTION.value, "key": encrypted_password,
             "data": additional_data,
             "algo": algorithm, "bits": bits})
        return data, password

    @classmethod
    def _create_handshake_block_base(cls, bits: int, public_key_received_for_encryption: str):
        """
        Creates base data for handshake block
        :param bits:
        :param public_key_received_for_encryption:
        :return:
        """
        byte_length = int(bits / 8)
        password = SecurePasswordGenerator(length=byte_length).generate().encode("utf-8")[:byte_length]
        pub_key = AsymCrypt.public_key_from_base64(public_key_received_for_encryption,
                                                   can_encrypt=True)
        encrypted_password_bytes = AsymCrypt.encrypt_message(pub_key,
                                                             password)
        encrypted_password = bytes_to_base64(encrypted_password_bytes)
        return encrypted_password, password

    @classmethod
    def create_handshake_encryption_block_dict(cls,
                                               public_key_received_for_encryption: str,
                                               bits: int = 192, algorithm: str = "AES",
                                               additional_data: str = "") -> (dict, bytes):
        """
        Create handshake encryption data for block
        :param additional_data:
        :param public_key_received_for_encryption:
        :param bits:
        :param algorithm:
        :return: handshake block in dict format, password
        """
        encrypted_password, password = cls._create_handshake_block_base(bits,
                                                                        public_key_received_for_encryption)

        data = {"cmd": CMD.HANDSHAKE_ENCRYPTION.value,
                "key": encrypted_password,
                "data": additional_data,
                "algo": algorithm, "bits": bits}
        return data, password

    def get_last(self):
        return self.chain[-1]

    @staticmethod
    def get_next_work_required(requested_diff: Difficulty) -> int:
        """

        Get Required work from Difficulty parameters
        @param requested_diff Input Difficulty
        @return

        :param requested_diff:
        :return:
        """
        return 1 << requested_diff.n_bits

    def validate_next_block(self, block: Block):

        if block.index != 0 and block.index != self.get_last().index + 1:
            logger.error(
                f"Block index is not same as chain length {block.index} != {len(self.chain)}")
            return False

        if block.index > 0 and block.previous_hash != (cb := self.get_last().hash.value):
            logger.error(
                f"Previous hash is not correct {block.previous_hash.hex()} != {cb.hex()}")
            return False

        # Check if the hash satisfies the difficulty requirements
        block_hash = block.compute_hash()
        block_z_bits = PowUtils.get_bit_length(block_hash, block.nonce, block.diff)
        target_bits = self.difficulty.hash_len_chars * 8 - self.difficulty.n_bits

        if block_z_bits > target_bits:
            logger.debug("Block hash %s %s nonce %s" % (block_hash.value_as_hex(), block_z_bits, block.nonce))
            logger.error(
                f"Mined block was not mined with correct difficulty, or not mined properly {block_z_bits} b > {target_bits}")
            return False

        if block.diff != self.difficulty:
            logger.error(
                f"Block difficulty is not same, Block: {block.diff} != Blockchain: {self.difficulty}")
            return False

        # Check if the timestamp is greater than the last block's timestamp
        # IDK if this check should be here
        if block.index > 0 and block.timestamp < self.get_last().timestamp - 1.5:
            logger.error(
                f"Timestamp is traveling back in time {block.timestamp} < {self.get_last().timestamp}")
            return False

        return True

    def clear(self):
        self.chain.clear()

    def insert(self, block: Block):
        if RUN_IN_DEBUG:
            t = Timer()

        if self.validate_next_block(block):
            if RUN_IN_DEBUG:
                logger.debug("Validation took %s ms" % (t.stop()))
            self.chain.append(block)

            if RUN_IN_DEBUG:
                logger.debug("Append took %s ms" % (t.stop()))

            if self.save:
                asyncio.run(self._save_block(block))
            if RUN_IN_DEBUG:
                logger.debug("Inserted! %s into %s" % (block, self.name))
            return True
        logger.error(f"Block {block} validation failed")
        logger.error(f"Blockchain that has failed to insert block \n{self}")
        return False

    def __str__(self):
        out = f"Name: {self.name} | ID: {self.id} | Blockchain Version: {self.version}  | Blocks:\n"
        for block in self.chain:
            out += f"{block}"
        return out

    def template_next_block(self, requested_diff: Difficulty, data: bytes | bytearray):
        """
        Template a new block without setting a new difficulty
        :param requested_diff:
        :param data:
        :return:
        """
        logger.debug("Templated next block with difficulty %s" % requested_diff)
        last = self.get_last()
        return Block(last.index + 1, last.hash.value, requested_diff, data, do_metric=self.do_metric)

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value: Difficulty):
        self._difficulty = value
        logger.debug(f"Set new blockchain difficulty {value}")
        if self.do_metric:
            try:
                loop = asyncio.get_running_loop()  # Try to get the current event loop
                # If we're inside an event loop, schedule tasks
                loop.create_task(send_metric("block_difficulty_bits", value.n_bits))
                loop.create_task(send_metric("block_difficulty_time", value.t_cost))
                loop.create_task(send_metric("block_difficulty_memory", value.m_cost))
                loop.create_task(send_metric("block_difficulty_parallel", value.p_cost))
            except RuntimeError:  # If there is no running loop, handle it
                # Create a new event loop and run the coroutines
                asyncio.run(send_metric("block_difficulty_bits", value.n_bits))
                asyncio.run(send_metric("block_difficulty_time", value.t_cost))
                asyncio.run(send_metric("block_difficulty_memory", value.m_cost))
                asyncio.run(send_metric("block_difficulty_parallel", value.p_cost))

    async def _save_block(self, block):
        async with session_scope() as session:
            # Create a new BlockTable entry
            bdb = BlockTable(
                blockchain_id=self._id,
                index=block.index,
                hash=bytearray(block.hash.value),
                previous_hash=block.previous_hash,
                data=block.data,
                nonce=block.nonce
            )
            session.add(bdb)

            # Flush the session asynchronously to persist the block and get its ID
            await session.flush()

            # If the block has a signature, save it in the BlockSignatureTable
            if block.signature:
                bst = BlockSignatureTable(
                    block_id=bdb.block_id,
                    signature=KeyManager.key_to_base64(block.signature)
                )
                session.add(bst)

            # Commit the transaction asynchronously
            await session.commit()

    @property
    def id(self):
        return self._id
