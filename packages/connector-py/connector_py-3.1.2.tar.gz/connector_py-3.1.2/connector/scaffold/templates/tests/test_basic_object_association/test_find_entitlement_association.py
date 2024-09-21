import pytest
import pytest_cases

from connector.oai.capability import CapabilityName, get_oauth
from {name}.serializers.request import (
    {pascal}FindEntitlementAssociationsRequest,
)
from connector.generated import (
    FindEntitlementAssociationsResponse,
    Error,
    ErrorCode,
    ErrorResponse,
)
from {name}.integration import integration

from tests.conftest import ClientContextManager, ResponseBodyMap

@pytest.mark.skip(reason="Function not implemented yet, remove after implementation of tested function.")
@pytest_cases.parametrize_with_cases(
    ["args", "response_body_map", "expected_response"],
    cases=[
        "tests.test_basic_object_association.test_find_entitlement_association_cases",
    ],
)
def test_find_entitlement_association(
    httpx_async_client: ClientContextManager,
    args: {pascal}FindEntitlementAssociationsRequest,
    response_body_map: ResponseBodyMap,
    expected_response: FindEntitlementAssociationsResponse | ErrorResponse,
) -> None:
    """Test ``find_entitlement_associations`` operation."""
    with httpx_async_client(get_oauth(args).access_token, response_body_map):
        response = integration.dispatch(CapabilityName.FIND_ENTITLEMENT_ASSOCIATIONS, args.model_dump_json())

    assert response == expected_response.model_dump_json()
