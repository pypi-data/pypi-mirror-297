import base64

from dharitri_sdk.core.address import Address
from dharitri_sdk.core.transactions_outcome_parsers.delegation_transactions_outcome_parser import \
    DelegationTransactionsOutcomeParser
from dharitri_sdk.core.transactions_outcome_parsers.resources import (
    SmartContractResult, TransactionEvent, TransactionLogs, TransactionOutcome)
from dharitri_sdk.testutils.utils import base64_topics_to_bytes


class TestDelegationTransactionsOutcomeParser:
    parser = DelegationTransactionsOutcomeParser()

    def test_parse_create_new_delegation_contract(self):
        contract_address = Address.new_from_bech32("moa1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqy8llllshjzgvy")

        encodedTopics = [
            "Q8M8GTdWSAAA",
            "Q8M8GTdWSAAA",
            "AQ==",
            "Q8M8GTdWSAAA",
            "AAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAABD///8=",
        ]

        delegate_event = TransactionEvent(
            address="moa18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqevhvh6",
            identifier="delegate",
            topics=base64_topics_to_bytes(encodedTopics)
        )

        encodedTopics = [
            "AAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAABD///8=",
            "PDXX6ssamaSgzKpTfvDMCuEJ9B9sK0AiA+Yzv7sHH1w=",
        ]

        sc_deploy_event = TransactionEvent(
            address="moa1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqy8llllshjzgvy",
            identifier="SCDeploy",
            topics=base64_topics_to_bytes(encodedTopics)
        )

        logs = TransactionLogs(events=[delegate_event, sc_deploy_event])

        encoded_topics = ["b2g6sUl6beG17FCUIkFwCOTGJjoJJi5SjkP2077e6xA="]
        sc_result_event = TransactionEvent(
            address="moa18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqevhvh6",
            identifier="completedTxEvent",
            topics=base64_topics_to_bytes(encoded_topics)
        )

        sc_result_log = TransactionLogs(
            address="moa18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqevhvh6",
            events=[sc_result_event]
        )

        sc_result = SmartContractResult(
            sender="moa1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqylllsjrx4c2",
            receiver="moa18s6a06ktr2v6fgxv4ffhauxvptssnaqlds45qgsrucemlwc8rawqevhvh6",
            data=base64.b64decode("QDZmNmJAMDAwMDAwMDAwMDAwMDAwMDAwMDEwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxMGZmZmZmZg=="),
            logs=sc_result_log
        )

        tx_outcome = TransactionOutcome(transaction_results=[sc_result], transaction_logs=logs)

        outcome = self.parser.parse_create_new_delegation_contract(tx_outcome)

        assert len(outcome) == 1
        assert outcome[0].contract_address == contract_address.to_bech32()
