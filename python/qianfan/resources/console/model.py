# Copyright (c) 2023 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Model API
"""

from typing import Any, Dict, List, Optional, Union

from qianfan.consts import Consts
from qianfan.resources.console.consts import (
    EvaluationResultExportDestinationType,
    EvaluationResultExportField,
    EvaluationResultExportRange,
    ModelTypePreset,
    ModelTypeUser,
)
from qianfan.resources.console.utils import console_api_request
from qianfan.resources.typing import QfRequest


class Model(object):
    """
    Class for Model Management API
    """

    @classmethod
    @console_api_request
    def list(cls, model_id: str, **kwargs: Any) -> QfRequest:
        """
        List all versions and source information of a model.

        This class method is used to retrieve information about all versions of a
        specific model, along with their source details.

        Parameters:
          model_id (str):
            The unique identifier of the model for which you want to list versions.
          kwargs (Any):
            Additional keyword arguments that can be passed to customize the request.

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.

        API Doc: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/clnlizwcs
        """
        req = QfRequest(method="POST", url=Consts.ModelDetailAPI)
        req.json_body = {"modelId": model_id, **kwargs}
        return req

    @classmethod
    @console_api_request
    def detail(cls, model_version_id: str, **kwargs: Any) -> QfRequest:
        """
        Retrieve detailed information for a specific model version.

        This method is used to fetch detailed information about a particular model
        version identified by the `model_version_id` parameter. The information
        includes various attributes and properties associated with the specified
        model version.

        Parameters:
          model_version_id (str):
            The unique identifier for the model version whose details are to be
            retrieved.
          kwargs (Any):
            Additional keyword arguments that can be passed to customize the request.

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.

        API Doc: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/ylnljj3ku
        """
        req = QfRequest(method="POST", url=Consts.ModelVersionDetailAPI)
        req.json_body = {"modelVersionId": model_version_id, **kwargs}
        return req

    @classmethod
    @console_api_request
    def publish(
        cls,
        is_new: bool,
        version_meta: Dict[str, Any],
        model_name: Optional[str] = None,
        model_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> QfRequest:
        """
        Publishes a trained model to the model repository.

        This function allows for the publishing of a trained model to a model
        repository.

        Parameters:
          is_new (bool):
            A boolean indicating whether this is a new model to be published.
          version_meta (Dict[str, Any]):
            Metadata for the model being published, including description, jobId,
            taskId, step.
          model_name (Optional[str]):
            The name of the model to be published (required when `is_new` is True).
          model_id (Optional[str]):
            The ID of the model to be published (required when `is_new` is False).
          tags (Optional[List[str]]):
            A list of tags associated with the model (optional).
          kwargs (Any):
            Additional keyword arguments that can be passed to customize the request.

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.

        API Doc: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Jlnlm0rdx
        """
        req = QfRequest(method="POST", url=Consts.ModelPublishAPI)
        req.json_body = {"isNewModel": is_new, "versionMeta": version_meta, **kwargs}
        if model_name is not None:
            req.json_body["modelName"] = model_name
        if model_id is not None:
            req.json_body["modelId"] = model_id
        if tags is not None:
            req.json_body["tags"] = tags
        return req

    @classmethod
    @console_api_request
    def create_evaluation_task(
        cls,
        name: str,
        version_info: List[Dict[str, Any]],
        dataset_id: str,
        eval_config: Dict[str, Any],
        description: Optional[str] = None,
        pending_eval_id: Optional[int] = None,
        **kwargs: Any,
    ) -> QfRequest:
        """
        Create an evaluation task on model(s) with dataset

        Parameters:
            name (str):
                the evaluation name you want to use
            version_info (List[Dict[str, Any]]):
                a list of model info which will be evaluated
            dataset_id (str):
                dataset's id for evaluation
            eval_config (Dict[str, Any]):
                the detail info about how to conduct this evaluation
            description (Optional[str]):
                description about evaluation, default to None.
            pending_eval_id (Optional[int]):
                the id of evaluation which doesn't start yet,
                you can set this parameter to modify the spec of
                specific evaluation and start it. Default to None
            **kwargs (Any):
                arbitrary arguments

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.

        API Doc: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/Hlpbyhl9o
        """
        req = QfRequest(method="POST", url=Consts.ModelEvalCreateAPI)
        request_json: Dict[str, Any] = {
            "name": name,
            "versionEvalInfo": version_info,
            "datasetId": dataset_id,
            "evalStandardConf": eval_config,
            "computeResourceConf": {"vmType": 1, "vmNumber": 8},
        }

        if pending_eval_id:
            request_json["id"] = pending_eval_id

        if description:
            request_json["description"] = description

        req.json_body = request_json
        return req

    @classmethod
    @console_api_request
    def get_evaluation_info(
        cls,
        eval_id: str,
        **kwargs: Any,
    ) -> QfRequest:
        """
        Get an evaluation task info

        Parameters:
            eval_id (str):
                the id of evaluation you want to check
            **kwargs (Any):
                arbitrary arguments

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.

        API Doc: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/wlpbyj1dn
        """
        req = QfRequest(method="POST", url=Consts.ModelEvalInfoAPI)
        req.json_body = {"id": eval_id}

        return req

    @classmethod
    @console_api_request
    def get_evaluation_result(
        cls,
        eval_id: str,
        **kwargs: Any,
    ) -> QfRequest:
        """
        Get the result of an evaluation

        Parameters:
            eval_id (str):
                the id of evaluation you want to check
            **kwargs (Any):
                arbitrary arguments

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.

        API Doc: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/7lpbyk8fj
        """
        req = QfRequest(method="POST", url=Consts.ModelEvalResultAPI)
        req.json_body = {"id": eval_id}

        return req

    @classmethod
    @console_api_request
    def stop_evaluation_task(
        cls,
        eval_id: str,
        **kwargs: Any,
    ) -> QfRequest:
        """
        Stop an evaluation task

        Parameters:
            eval_id (str):
                the id of evaluation you want to stop
            **kwargs (Any):
                arbitrary arguments

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.

        API Doc: https://cloud.baidu.com/doc/WENXINWORKSHOP/s/klpbyl1ea
        """
        req = QfRequest(method="POST", url=Consts.ModelEvalStopAPI)
        req.json_body = {"id": eval_id}

        return req

    @classmethod
    @console_api_request
    def create_evaluation_result_export_task(
        cls,
        eval_id: Union[str, int],
        export_destination_type: Optional[EvaluationResultExportDestinationType] = None,
        export_range: EvaluationResultExportRange = EvaluationResultExportRange.Total,
        export_field: Optional[List[EvaluationResultExportField]] = None,
        bos_bucket_id: Optional[str] = None,
        result_ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> QfRequest:
        """
        Create evaluation result export task

        Parameters:
            eval_id (Union[str, int]):
                the id of evaluation you want to export
            export_destination_type (Optional[EvaluationResultExportDestinationType]):
                where to export evaluation result, default to
                EvaluationResultExportDestinationType.PublicBos
            export_range (EvaluationResultExportRange):
                which part of evaluation result should be exported, default to
                EvaluationResultExportRange.Total
            export_field (Optional[List[EvaluationResultExportField]]):
                which field should be contained in exported data, default to all.
            bos_bucket_id (Optional[str]):
                bucket id of your private bos, used when export_destination_type is
                EvaluationResultExportDestinationType.PrivateBos. Default to None
            result_ids (Optional[List[str]]):
                which results you want to export, used when export_range is
                EvaluationResultExportRange.Part. Default to None
            **kwargs (Any):
                arbitrary arguments

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.

        Not available currently
        """
        if not export_destination_type:
            export_destination_type = EvaluationResultExportDestinationType.PublicBos

        if not export_field:
            export_field = [
                EvaluationResultExportField.Prompt,
                EvaluationResultExportField.Prediction,
                EvaluationResultExportField.Completion,
                EvaluationResultExportField.Metrics,
            ]

        request_json = {
            "id": eval_id,
            "exportType": export_destination_type.value,
            "exportOpt": export_range.value,
            "exportContent": [field.value for field in export_field],
        }

        if export_destination_type == EvaluationResultExportDestinationType.PrivateBos:
            if not bos_bucket_id:
                raise ValueError("export to private bos without bos bucket id")
            request_json["volumeId"] = bos_bucket_id

        if export_range == EvaluationResultExportRange.Part:
            if not result_ids:
                raise ValueError("doing export partially without result id list")
            request_json["resultIds"] = result_ids

        req = QfRequest(method="POST", url=Consts.ModelEvalResultExportAPI)
        req.json_body = request_json

        return req

    @classmethod
    @console_api_request
    def get_evaluation_result_export_task_status(
        cls,
        export_task_id: Union[str, int],
        **kwargs: Any,
    ) -> QfRequest:
        """
        Get evaluation result export task status

        Parameters:
            export_task_id (Union[str, int]):
                export task id
            **kwargs (Any):
                arbitrary arguments

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.

        Not available currently
        """
        return QfRequest(
            method="POST",
            url=Consts.ModelEvalResultExportStatusAPI,
            json_body={
                "exportID": export_task_id,
            },
        )

    @classmethod
    @console_api_request
    def preset_list(
        self,
        name_filter: Optional[str] = None,
        model_type: Optional[List[ModelTypePreset]] = None,
        model_version_vendor: Optional[List[str]] = None,
        ctx_length: Optional[List[str]] = None,
        language_support: Optional[List[str]] = None,
        expansion: Optional[List[str]] = None,
        order_by: Optional[str] = None,
        page_no: int = 1,
        page_size: int = 20,
        **kwargs: Any,
    ) -> QfRequest:
        """
        Get the list of preset models

        Parameters:
            name_filter (Optional[str]):
                name filter to filter preset models
            model_type (Optional[List[ModelTypePreset]]):
                model type to filter preset models
            model_version_vendor (Optional[List[str]]):
                model version vendor to filter preset models
            ctx_length (Optional[List[str]]):
                context length to filter preset models
            language_support (Optional[List[str]]):
                language support to filter preset models
            expansion (Optional[List[str]]):
                expansion to filter preset models
            order_by (Optional[str]):
                order to filter preset models
            page_no (int):
                page number default is 1, start from 1
            page_size (int):
                page size default is 20
            **kwargs (Any):
                arbitrary arguments

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.

        """
        req = QfRequest(method="POST", url=Consts.ModelPresetListAPI)
        req.json_body = {"pageNo": page_no, "pageSize": page_size}
        if name_filter:
            req.json_body["nameFilter"] = name_filter
        if model_type:
            req.json_body["modelType"] = model_type
        if model_version_vendor:
            req.json_body["modelVersionVendor"] = model_version_vendor
        if ctx_length:
            req.json_body["ctxLength"] = ctx_length
        if language_support:
            req.json_body["languageSupport"] = language_support
        if expansion:
            req.json_body["expansion"] = expansion
        if order_by:
            req.json_body["orderBy"] = order_by

        return req

    @classmethod
    @console_api_request
    def user_list(
        cls,
        name_filter: Optional[str] = None,
        model_type: Optional[List[ModelTypeUser]] = None,
        order_by: Optional[str] = None,
        order: Optional[str] = None,
        page_no: int = 1,
        page_size: int = 20,
        **kwargs: Any,
    ) -> QfRequest:
        """
        Get the list of user models

        Parameters:
            name_filter (Optional[str]):
                name filter to filter preset models
            model_type (Optional[List[ModelTypeUser]]):
                model type to filter preset models
            order_by (Optional[str]):
                order condition, such as `create_time`
            order (Optional[str]):
                order type, including: `asc` and `desc`
            page_no (int):
                page number default is 1, start from 1
            page_size (int):
                page size default is 20
            **kwargs (Any):
                arbitrary arguments

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.

        """
        req = QfRequest(method="POST", url=Consts.ModelUserListAPI)
        req.json_body = {"pageNo": page_no, "pageSize": page_size}
        if name_filter:
            req.json_body["nameFilter"] = name_filter
        if model_type:
            req.json_body["modelType"] = model_type
        if order_by:
            req.json_body["orderBy"] = order_by
        if order:
            req.json_body["order"] = order

        return req

    @classmethod
    @console_api_request
    def batch_delete_model(
        cls,
        model_ids: Union[List[int], List[str]],
        **kwargs: Any,
    ) -> QfRequest:
        """
        batch delete model by ids

        Parameters:
            model_ids (Union[List[int], List[str]]):
                model ids to delete
            **kwargs (Any):
                arbitrary arguments

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.

        """
        req = QfRequest(method="POST", url=Consts.ModelBatchDeleteAPI)
        req.json_body = {"modelIDs": model_ids}

        return req

    @classmethod
    @console_api_request
    def batch_delete_model_version(
        cls,
        model_version_ids: Union[List[int], List[str]],
        **kwargs: Any,
    ) -> QfRequest:
        """
        batch delete model version by ids

        Parameters:
            model_version_ids (Union[List[int], List[str]]):
                model version ids to delete
            **kwargs (Any):
                arbitrary arguments
        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.
        """
        req = QfRequest(method="POST", url=Consts.ModelVersionBatchDeleteAPI)
        req.json_body = {"modelVersionIds": model_version_ids}

        return req

    @classmethod
    @console_api_request
    def evaluable_model_list(
        cls,
        **kwargs: Any,
    ) -> QfRequest:
        """
        get all evaluable model list

        Parameters:
            **kwargs (Any):
                arbitrary arguments

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.
        """

        req = QfRequest(method="POST", url=Consts.ModelEvaluableModelListAPI)
        return req

    @classmethod
    @console_api_request
    def get_evaluation_result_list(
        cls,
        id: Union[str, int],
        bleu4: Optional[Dict[str, float]] = None,
        rouge_1: Optional[Dict[str, float]] = None,
        rouge_2: Optional[Dict[str, float]] = None,
        rouge_l: Optional[Dict[str, float]] = None,
        judge_score: Optional[Dict[str, int]] = None,
        model_version_ids: Optional[List[int]] = None,
        order_by: Optional[str] = None,
        order: Optional[str] = None,
        eval_unit_id: Optional[List[str]] = None,
        page_no: int = 1,
        page_size: int = 20,
        **kwargs: Any,
    ) -> QfRequest:
        """
        Get the list of user models

        Parameters:
            id (Union[str, int]):
                evaluation id
            bleu4 (Optional[float]):
                bleu4 score, {"start": 0.0, "end": 1.0}
            rouge_1 (Optional[float]):
                rouge_1 score, {"start": 0.0, "end": 1.0}
            rouge_2 (Optional[float]):
                rouge_2 score, {"start": 0.0, "end": 1.0}
            rouge_l (Optional[float]):
                rouge_l score, {"start": 0.0, "end": 1.0}
            judge_score (Optional[int]):
                judge score, {"start": -1, "end": ...}
            model_version_ids (Optional[List[int]]):
                model version ids
            order_by (Optional[str]):
                order condition, such as `bleu4`
            order (Optional[str]):
                order type, including: `asc` and `desc`
            eval_unit_id (Optional[List[str]]):
                evaluation unit ids
            page_no (int):
                page number default is 1, start from 1
            page_size (int):
                page size default is 20
            **kwargs (Any):
                arbitrary arguments

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.

        """
        req = QfRequest(method="POST", url=Consts.ModelEvalResultListAPI)
        req.json_body = {"id": id, "pageNo": page_no, "pageSize": page_size}
        if bleu4:
            req.json_body["bleu4"] = bleu4
        if rouge_1:
            req.json_body["rouge_1"] = rouge_1
        if rouge_2:
            req.json_body["rouge_2"] = rouge_2
        if rouge_l:
            req.json_body["rouge_l"] = rouge_l
        if judge_score:
            req.json_body["judgeScore"] = judge_score
        if model_version_ids:
            req.json_body["modelVersionIds"] = model_version_ids
        if eval_unit_id:
            req.json_body["evalUnitId"] = eval_unit_id
        if order_by:
            req.json_body["orderBy"] = order_by
        if order:
            req.json_body["order"] = order

        return req

    @classmethod
    @console_api_request
    def batch_delete_evaluation_result(
        cls,
        eval_ids: Union[List[str], List[int]],
        **kwargs: Any,
    ) -> QfRequest:
        """
        Get the list of user models

        Parameters:
            eval_ids (Union[List[str], List[int]]):
                evaluation result ids to delete
            **kwargs (Any):
                arbitrary arguments

        Note:
        The `@console_api_request` decorator is applied to this method, enabling it to
        send the generated QfRequest and return a QfResponse to the user.

        """
        req = QfRequest(method="POST", url=Consts.ModelEvalResultBatchDeleteAPI)
        req.json_body = {"evalIds": eval_ids}

        return req
