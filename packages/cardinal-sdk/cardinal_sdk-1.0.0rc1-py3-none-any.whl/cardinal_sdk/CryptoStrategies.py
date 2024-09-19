import base64
import json
from dataclasses import dataclass
from enum import Enum
from cardinal_sdk.model import serialize_data_owner_with_type, deserialize_data_owner_with_type, CryptoActorStubWithType, DataOwnerWithType, RecoveryDataUseFailureReason, deserialize_recovery_result, RecoveryResultFailure
from cardinal_sdk.model.specializations import SpkiHexString, KeypairFingerprintV1String
from cardinal_sdk.model.SingletonMeta import SingletonMeta
from cardinal_sdk.model.CallResult import create_result_from_json
from typing import Dict, List, Union, Callable, Optional
from abc import ABC, abstractmethod
from ctypes import c_void_p, CFUNCTYPE, c_char_p, cast
import traceback
from cardinal_sdk.kotlin_types import symbols


@dataclass
class KeyDataRecoveryRequest:
    """
    A request to recover key data that was not found for a user.

    Args:
        data_owner_details (DataOwnerWithType): The data owner for which the key data should be recovered.
        unknown_keys (List[SpkiHexString]): ll public keys (in hex-encoded spki format) of `dataOwner` for which the
            authenticity status (verified or unverified) is unknown (no result was cached from a previous api
            instantiation and the key was not generated on the current device). This could include keys that were
            recovered automatically by the sdk and may have overlap with `unavailableKeys`.
        unavailable_keys (List[SpkiHexString]): All public keys (in hex-encoded spki format) of `dataOwner` for which
            the sdk could not recover a private key. May overlap (partially or completely) with `unknownKeys`.
    """
    data_owner_details: DataOwnerWithType
    unknown_keys: List[SpkiHexString]
    unavailable_keys: List[SpkiHexString]

    def __serialize__(self) -> object:
        return {
            "dataOwnerDetails": serialize_data_owner_with_type(self.data_owner_details),
            "unknownKeys": self.unknown_keys,
            "unavailableKeys": self.unavailable_keys
        }

    @classmethod
    def _deserialize(cls, data: Union[str, Dict[str, object]]) -> 'KeyDataRecoveryRequest':
        deserialized_dict: dict[str, object]
        if isinstance(data, str):
            deserialized_dict = json.loads(data)
        else:
            deserialized_dict = data
        return cls(
            data_owner_details=deserialize_data_owner_with_type(deserialized_dict["dataOwnerDetails"]),
            unknown_keys=deserialized_dict["unknownKeys"],
            unavailable_keys=deserialized_dict["unavailableKeys"]
        )


"""
Specifies how the SDK should behave when a new key pair is required for a data owner.
"""
KeyGenerationRequestResult = Union['KeyGenerationRequestResultAllow', 'KeyGenerationRequestResultDeny', 'KeyGenerationRequestResultUse']


class KeyGenerationRequestResultAllow(metaclass=SingletonMeta):
    """
    Allows the SDK to generate a new key pair for the current data owner.
    """

    def __serialize__(self) -> object:
        return {}

    @classmethod
    def _deserialize(cls, data: Union[str, Dict[str, object]]) -> 'KeyGenerationRequestResultAllow':
        return cls()


class KeyGenerationRequestResultDeny(metaclass=SingletonMeta):
    """
    The SDK must not generate a new key for the data owner. The SDK initialisation should fail with a predefined error.
    """

    def __serialize__(self) -> object:
        return {}

    @classmethod
    def _deserialize(cls, data: Union[str, Dict[str, object]]) -> 'KeyGenerationRequestResultDeny':
        return cls()


@dataclass
class KeyGenerationRequestResultUse:
    """
    The SDK should use the provided key pair as a new key for the data owner.

    Args:
        key_pkcs8 (bytearray): The key pair to provide, as byte array.
    """

    key_pkcs8: bytearray

    def __serialize__(self) -> object:
        return {
            "keyPkcs8": base64.b64encode(self.key_pkcs8).decode('utf-8')
        }

    @classmethod
    def _deserialize(cls, data: Union[str, Dict[str, object]]) -> 'KeyGenerationRequestResultUse':
        deserialized_dict: dict[str, object]
        if isinstance(data, str):
            deserialized_dict = json.loads(data)
        else:
            deserialized_dict = data
        return cls(
            key_pkcs8=bytearray(base64.b64decode(deserialized_dict["keyPkcs8"]))
        )


def serialize_key_generation_request_result(key_generation_request_result: KeyGenerationRequestResult) -> object:
    if isinstance(key_generation_request_result, KeyGenerationRequestResultAllow):
        serialized_entity = key_generation_request_result.__serialize__()
        serialized_entity.update({"type": "com.icure.cardinal.sdk.py.PyCryptoStrategies.PyKeyGenerationRequestResult.Allow"})
        return serialized_entity
    elif isinstance(key_generation_request_result, KeyGenerationRequestResultDeny):
        serialized_entity = key_generation_request_result.__serialize__()
        serialized_entity.update({"type": "com.icure.cardinal.sdk.py.PyCryptoStrategies.PyKeyGenerationRequestResult.Deny"})
        return serialized_entity
    elif isinstance(key_generation_request_result, KeyGenerationRequestResultUse):
        serialized_entity = key_generation_request_result.__serialize__()
        serialized_entity.update({"type": "com.icure.cardinal.sdk.py.PyCryptoStrategies.PyKeyGenerationRequestResult.Use"})
        return serialized_entity
    else:
        raise Exception(f"{type(key_generation_request_result)} is not a known subclass of KeyGenerationRequestResult")


def deserialize_key_generation_request_result(data: Union[str, Dict[str, object]]) -> object:
    deserialized_dict: dict[str, object]
    if isinstance(data, str):
        deserialized_dict = json.loads(data)
    else:
        deserialized_dict = data
    qualifier = deserialized_dict.get("type")
    if qualifier is None:
        raise Exception("Missing qualifier: type")
    if qualifier == "com.icure.cardinal.sdk.py.PyCryptoStrategies.PyKeyGenerationRequestResult.Allow":
        return KeyGenerationRequestResultAllow._deserialize(deserialized_dict)
    elif qualifier == "com.icure.cardinal.sdk.py.PyCryptoStrategies.PyKeyGenerationRequestResult.Deny":
        return KeyGenerationRequestResultDeny._deserialize(deserialized_dict)
    elif qualifier == "com.icure.cardinal.sdk.py.PyCryptoStrategies.PyKeyGenerationRequestResult.Use":
        return KeyGenerationRequestResultUse._deserialize(deserialized_dict)
    else:
        raise Exception(f"{qualifier} is not a known subclass of DataOwnerWithType")


class RsaEncryptionAlgorithm(Enum):
    """
    Represents the encryption algorith used to generate the ExportedKeyData.
    """

    OaepWithSha1 = "OaepWithSha1"
    OaepWithSha256 = "OaepWithSha256"

    def __serialize__(self) -> object:
        return self.value

    @classmethod
    def _deserialize(cls, data: Union[str, Dict[str, object]]) -> 'RsaEncryptionAlgorithm':
        if data == "OaepWithSha1":
            return RsaEncryptionAlgorithm.OaepWithSha1
        elif data == "OaepWithSha256":
            return RsaEncryptionAlgorithm.OaepWithSha256
        else:
            raise Exception(f"{data} is not a valid value for RsaEncryptionAlgorithm enum.")


@dataclass
class ExportedKeyData:
    """
    Represents a private key with the algorithm used to generate it.
    """
    private_key_pkcs8: bytearray
    algorithm: RsaEncryptionAlgorithm

    def __serialize__(self) -> object:
        return {
            "private": base64.b64encode(self.private_key_pkcs8).decode('utf-8'),
            "algorithm": self.algorithm.__serialize__()
        }

    @classmethod
    def _deserialize(cls, data: Union[str, Dict[str, object]]) -> 'ExportedKeyData':
        deserialized_dict: dict[str, object]
        if isinstance(data, str):
            deserialized_dict = json.loads(data)
        else:
            deserialized_dict = data
        return cls(
            private_key_pkcs8=bytearray(base64.b64decode(deserialized_dict["private"])),
            algorithm=RsaEncryptionAlgorithm._deserialize(deserialized_dict["algorithm"])
        )


@dataclass
class RecoveredKeyData:
    """
    Data recovered for a data owner.

    Args:
        recovered_keys (Dict[KeypairFingerprintV1String, RsaKeyPair]): All keys recovered for the data owner (will be
            automatically considered as verified), by fingerprint.
        key_authenticity (Dict[KeypairFingerprintV1String, bool]): associates each public key fingerprint its
            authenticity. Note that if any of the keys from `unknownKeys` is completely missing from this object the
            key will be considered as unverified in this api instance (same as if associated to false), but this value
            won't be cached (will be again part of `unknownKeys` in future instances.
    """
    recovered_keys: Dict[KeypairFingerprintV1String, ExportedKeyData]
    key_authenticity: Dict[KeypairFingerprintV1String, bool]

    def __serialize__(self) -> object:
        return {
            "recoveredKeys": {k: v.__serialize__() for k, v in self.recovered_keys.items()},
            "keyAuthenticity": self.key_authenticity
        }

    @classmethod
    def _deserialize(cls, data: Union[str, Dict[str, object]]) -> 'RecoveredKeyData':
        deserialized_dict: dict[str, object]
        if isinstance(data, str):
            deserialized_dict = json.loads(data)
        else:
            deserialized_dict = data
        return cls(
            recovered_keys={k: ExportedKeyData._deserialize(v) for k, v in deserialized_dict["recoveredKeys"].items()},
            key_authenticity=deserialized_dict["keyAuthenticity"]
        )

class CryptoStrategies(ABC):
    """
    Allows to customise the behaviour of the iCure SDK when performing cryptographic operations.
    """

    @abstractmethod
    def recover_and_verify_self_hierarchy_keys(
            self,
            keys_data: List[KeyDataRecoveryRequest],
            recover_with_icure_recovery_key: Callable[[str, bool], Union[Dict[str, Dict[str, ExportedKeyData]], RecoveryDataUseFailureReason]]
    ) -> Dict[str, RecoveredKeyData]:
        """
        Method called during initialisation of the crypto API to validate keys recovered through iCure's recovery methods and/or to allow recovery of
        missing keys using means external to iCure.
        On startup the iCure sdk will try to load all keys for the current data owner and its parent hierarchy: if the sdk can't find some of the keys
        for any of the data owners (according to the public keys for the data owner in the iCure server) and/or the sdk could recover some private keys
        but can't verify the authenticity of the key pairs this method will be called.
        The recovered and verified keys will automatically be cached using the current api {@link KeyStorageFacade} and {@link StorageFacade}

        The input is a list containing an object for each data owner part of the current data owner hierarchy. The objects are ordered from the data
        for the topmost parent of the current data owner hierarchy (first element) to the data for the current data owner (last element).

        :param keys_data all information on unknown and unavailable keys for each data owner part of the current data owner hierarchy.
        :param recover_with_icure_recovery_key allows to recover keypairs that were previously created using the RecoveryApi. This function
        takes in input the recovery key and if the corresponding recovery data should be deleted in case of successful recovery.
        In output in case of success this returns a dict data_owner_id (self or parent) -> public key spki hex -> corresponding key pair details.
        In case of recovery failure the output is the reason of the failure.
        :return a map that associates to each given data owner id the recovered data.
        """
        pass

    @abstractmethod
    def generate_new_key_for_data_owner(
            self,
            self_data_owner: DataOwnerWithType
    ) -> KeyGenerationRequestResult:
        """
        The correct initialisation of the crypto API requires that at least 1 verified (or device) key pair is available for each data owner part of the
        current data owner hierarchy. If no verified key is available for any of the data owner parents the api initialisation will automatically fail,
        however if there is no verified key for the current data owner you can instead create a new crypto key.
        :param self_data_owner the current data owner.
        :returns a KeyGenerationRequestResult specifying how the SDK should behave.
        """
        pass

    @abstractmethod
    def verify_delegate_public_keys(
            self,
            delegate: CryptoActorStubWithType,
            public_keys: List[str],
    ) -> List[str]:
        """
        Verifies if the public keys of a data owner which will be the delegate of a new exchange key do actually belong to the person the data owner
        represents. This method is not called when the delegate would be the current data owner for the api.

        The user will have to obtain the verified public keys of the delegate from outside iCure, for example by email with another hcp, by checking the
        personal website of the other user, or by scanning verification qr codes at the doctor office...

        As long as one of the public keys is verified the creation of a new exchange key will succeed. If no public key is verified the operation will
        fail.
        :param delegate the potential data owner delegate.
        :param public_keys public keys requiring verification, in spki hex-encoded format.
        :returns all verified public keys, in spki hex-encoded format.
        """
        pass

    @abstractmethod
    def data_owner_requires_anonymous_delegation(self, data_owner: CryptoActorStubWithType) -> bool:
        """
        Specifies if a data owner requires anonymous delegations, i.e. his id should not appear unencrypted in new secure delegations. This should always
        be the case for patient data owners.
        :param data_owner a data owner.
        :returns true if the delegations for the provided data owner should be anonymous.
        """
        pass

_C_RecoverAndVerifySelfHierarchyKeys = CFUNCTYPE(None, c_void_p, c_char_p, c_void_p)
_C_GenerateNewKeyForDataOwner = CFUNCTYPE(None, c_void_p, c_char_p)
_C_VerifyDelegatePublicKeys = CFUNCTYPE(None, c_void_p, c_char_p, c_char_p)
_C_DataOwnerRequiresAnonymousDelegation = CFUNCTYPE(None, c_void_p, c_char_p)

class _CryptoStrategiesBridge:
    __py_strategies: CryptoStrategies
    __CALLBACK_RecoverAndVerifySelfHierarchyKeys: _C_RecoverAndVerifySelfHierarchyKeys
    __CALLBACK_GenerateNewKeyForDataOwner: _C_GenerateNewKeyForDataOwner
    __CALLBACK_VerifyDelegatePublicKeys: _C_VerifyDelegatePublicKeys
    __CALLBACK_DataOwnerRequiresAnonymousDelegation: _C_DataOwnerRequiresAnonymousDelegation
    __kt_crypto_strategies: Optional[c_void_p]

    def __init__(self, py_strategies: CryptoStrategies):
        self.__kt_crypto_strategies = None
        self.__py_strategies = py_strategies

    def __del__(self):
        if self.__kt_crypto_strategies is not None:
            symbols.kotlin.root.com.icure.cardinal.sdk.py.utils.disposeStablePtr(self.__kt_crypto_strategies)

    def recover_and_verify_self_hierarchy_keys(self, result_holder, keys_data, key_pair_recoverer):
        try:
            keys_data_json = json.loads(cast(keys_data, c_char_p).value.decode('utf-8'))
            def use_key_pair_recover(recovery_key, auto_delete):
                result_bytes = symbols.kotlin.root.com.icure.cardinal.sdk.py.PyCryptoStrategies.recoverWithRecoveryKey(
                    key_pair_recoverer,
                    recovery_key.encode('utf-8'),
                    auto_delete
                )
                result = create_result_from_json(cast(result_bytes, c_char_p).value.decode('utf-8'))
                symbols.DisposeString(result_bytes)
                if result.failure is not None:
                    raise Exception(result.failure)
                recovery_result = deserialize_recovery_result(result.success)
                if isinstance(recovery_result, RecoveryResultFailure):
                    return recovery_result.reason
                return {
                    k: {
                        k1: ExportedKeyData._deserialize(v1) for k1, v1 in v.items()
                    } for k, v in recovery_result.data.items()
                }
            result = self.__py_strategies.recover_and_verify_self_hierarchy_keys(
                [KeyDataRecoveryRequest._deserialize(x) for x in keys_data_json],
                use_key_pair_recover
            )
            result_json = {
                k: v.__serialize__() for k, v in result.items()
            }
            symbols.kotlin.root.com.icure.cardinal.sdk.py.utils.setCallbackResult(result_holder, json.dumps(result_json).encode('utf-8'))
        except:
            symbols.kotlin.root.com.icure.cardinal.sdk.py.utils.setCallbackFailure(result_holder, traceback.format_exc().encode('utf-8'))

    def generate_new_key_for_data_owner(self, result_holder, self_data_owner):
        try:
            result = self.__py_strategies.generate_new_key_for_data_owner(
                deserialize_data_owner_with_type(cast(self_data_owner, c_char_p).value.decode('utf-8'))
            )
            result_json = serialize_key_generation_request_result(result)
            symbols.kotlin.root.com.icure.cardinal.sdk.py.utils.setCallbackResult(result_holder, json.dumps(result_json).encode('utf-8'))
        except:
            symbols.kotlin.root.com.icure.cardinal.sdk.py.utils.setCallbackFailure(result_holder, traceback.format_exc().encode('utf-8'))

    def verify_delegate_public_keys(self, result_holder, delegate, public_keys):
        try:
            result = self.__py_strategies.verify_delegate_public_keys(
                CryptoActorStubWithType._deserialize(cast(delegate, c_char_p).value.decode('utf-8')),
                json.loads(cast(public_keys, c_char_p).value.decode('utf-8'))
            )
            symbols.kotlin.root.com.icure.cardinal.sdk.py.utils.setCallbackResult(result_holder, json.dumps(result).encode('utf-8'))
        except:
            symbols.kotlin.root.com.icure.cardinal.sdk.py.utils.setCallbackFailure(result_holder, traceback.format_exc())

    def data_owner_requires_anonymous_delegation(self, result_holder, data_owner):
        try:
            result = self.__py_strategies.data_owner_requires_anonymous_delegation(
                CryptoActorStubWithType._deserialize(cast(data_owner, c_char_p).value.decode('utf-8'))
            )
            symbols.kotlin.root.com.icure.cardinal.sdk.py.utils.setCallbackResult(result_holder, json.dumps(result).encode('utf-8'))
        except:
            symbols.kotlin.root.com.icure.cardinal.sdk.py.utils.setCallbackFailure(result_holder, traceback.format_exc().encode('utf-8'))

    def get_kt(self) -> c_void_p:
        if self.__kt_crypto_strategies is None:
            self.__CALLBACK_RecoverAndVerifySelfHierarchyKeys = _C_RecoverAndVerifySelfHierarchyKeys(self.recover_and_verify_self_hierarchy_keys)
            self.__CALLBACK_GenerateNewKeyForDataOwner = _C_GenerateNewKeyForDataOwner(self.generate_new_key_for_data_owner)
            self.__CALLBACK_VerifyDelegatePublicKeys = _C_VerifyDelegatePublicKeys(self.verify_delegate_public_keys)
            self.__CALLBACK_DataOwnerRequiresAnonymousDelegation = _C_DataOwnerRequiresAnonymousDelegation(self.data_owner_requires_anonymous_delegation)
            self.__kt_crypto_strategies = symbols.kotlin.root.com.icure.cardinal.sdk.py.PyCryptoStrategies.create(
                self.__CALLBACK_RecoverAndVerifySelfHierarchyKeys,
                self.__CALLBACK_GenerateNewKeyForDataOwner,
                self.__CALLBACK_VerifyDelegatePublicKeys,
                self.__CALLBACK_DataOwnerRequiresAnonymousDelegation,
            )
        return self.__kt_crypto_strategies