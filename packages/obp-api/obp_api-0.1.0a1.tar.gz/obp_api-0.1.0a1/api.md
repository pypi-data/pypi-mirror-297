# Accounts

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts">client.accounts.<a href="./src/obp_api/resources/accounts/accounts.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/account_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}">client.accounts.<a href="./src/obp_api/resources/accounts/accounts.py">update</a>(account_id, \*, bank_id, \*\*<a href="src/obp_api/types/account_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/my/accounts">client.accounts.<a href="./src/obp_api/resources/accounts/accounts.py">list</a>() -> BinaryAPIResponse</code>
- <code title="post /obp/v5.1.0/account/check/scheme/iban">client.accounts.<a href="./src/obp_api/resources/accounts/accounts.py">check_iban</a>(\*\*<a href="src/obp_api/types/account_check_iban_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}">client.accounts.<a href="./src/obp_api/resources/accounts/accounts.py">create_label</a>(account_id, \*, bank_id, \*\*<a href="src/obp_api/types/account_create_label_params.py">params</a>) -> BinaryAPIResponse</code>

## Public

Methods:

- <code title="get /obp/v5.1.0/accounts/public">client.accounts.public.<a href="./src/obp_api/resources/accounts/public.py">list</a>() -> BinaryAPIResponse</code>

## View

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/account">client.accounts.view.<a href="./src/obp_api/resources/accounts/view/view.py">retrieve</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>

### Checkbook

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/checkbook/orders">client.accounts.view.checkbook.<a href="./src/obp_api/resources/accounts/view/checkbook.py">list</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>

### Counterparties

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/counterparties">client.accounts.view.counterparties.<a href="./src/obp_api/resources/accounts/view/counterparties/counterparties.py">create</a>(view_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/accounts/view/counterparty_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/counterparties/{COUNTERPARTY_ID}">client.accounts.view.counterparties.<a href="./src/obp_api/resources/accounts/view/counterparties/counterparties.py">retrieve</a>(counterparty_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/counterparties">client.accounts.view.counterparties.<a href="./src/obp_api/resources/accounts/view/counterparties/counterparties.py">list</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>
- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/counterparties/{COUNTERPARTY_ID}">client.accounts.view.counterparties.<a href="./src/obp_api/resources/accounts/view/counterparties/counterparties.py">delete</a>(counterparty_id, \*, bank_id, account_id, view_id) -> None</code>

## Views

### CreditCards

#### Orders

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/credit_cards/orders">client.accounts.views.credit_cards.orders.<a href="./src/obp_api/resources/accounts/views/credit_cards/orders.py">list</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>

### DirectDebits

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/direct-debit">client.accounts.views.direct_debits.<a href="./src/obp_api/resources/accounts/views/direct_debits.py">create</a>(view_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/accounts/views/direct_debit_create_params.py">params</a>) -> BinaryAPIResponse</code>

### FundsAvailable

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/funds-available">client.accounts.views.funds_available.<a href="./src/obp_api/resources/accounts/views/funds_available.py">retrieve</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>

### Metadata

#### Tags

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/metadata/tags">client.accounts.views.metadata.tags.<a href="./src/obp_api/resources/accounts/views/metadata/tags.py">create</a>(view_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/accounts/views/metadata/tag_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/metadata/tags">client.accounts.views.metadata.tags.<a href="./src/obp_api/resources/accounts/views/metadata/tags.py">list</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/metadata/tags/{TAG_ID}">client.accounts.views.metadata.tags.<a href="./src/obp_api/resources/accounts/views/metadata/tags.py">delete</a>(tag_id, \*, bank_id, account_id, view_id) -> None</code>

### Counterparties

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}">client.accounts.views.counterparties.<a href="./src/obp_api/resources/accounts/views/counterparties/counterparties.py">retrieve</a>(other_account_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts">client.accounts.views.counterparties.<a href="./src/obp_api/resources/accounts/views/counterparties/counterparties.py">list</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>

#### Metadata

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/metadata">client.accounts.views.counterparties.metadata.<a href="./src/obp_api/resources/accounts/views/counterparties/metadata.py">retrieve</a>(other_account_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/metadata/corporate_location">client.accounts.views.counterparties.metadata.<a href="./src/obp_api/resources/accounts/views/counterparties/metadata.py">update</a>(other_account_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/accounts/views/counterparties/metadata_update_params.py">params</a>) -> BinaryAPIResponse</code>

#### Limits

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}/counterparties/{COUNTERPARTY_ID}/limits">client.accounts.views.counterparties.limits.<a href="./src/obp_api/resources/accounts/views/counterparties/limits.py">create</a>(counterparty_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/accounts/views/counterparties/limit_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}/counterparties/{COUNTERPARTY_ID}/limits">client.accounts.views.counterparties.limits.<a href="./src/obp_api/resources/accounts/views/counterparties/limits.py">retrieve</a>(counterparty_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}/counterparties/{COUNTERPARTY_ID}/limits">client.accounts.views.counterparties.limits.<a href="./src/obp_api/resources/accounts/views/counterparties/limits.py">update</a>(counterparty_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/accounts/views/counterparties/limit_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}/counterparties/{COUNTERPARTY_ID}/limits">client.accounts.views.counterparties.limits.<a href="./src/obp_api/resources/accounts/views/counterparties/limits.py">delete</a>(counterparty_id, \*, bank_id, account_id, view_id) -> None</code>

### Balances

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}/balances">client.accounts.views.balances.<a href="./src/obp_api/resources/accounts/views/balances.py">retrieve</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>

### TargetViews

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}/target-views">client.accounts.views.target_views.<a href="./src/obp_api/resources/accounts/views/target_views.py">create</a>(view_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/accounts/views/target_view_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}/target-views/TARGET_VIEW_ID">client.accounts.views.target_views.<a href="./src/obp_api/resources/accounts/views/target_views.py">retrieve</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}/target-views/TARGET_VIEW_ID">client.accounts.views.target_views.<a href="./src/obp_api/resources/accounts/views/target_views.py">update</a>(view_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/accounts/views/target_view_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}/target-views/TARGET_VIEW_ID">client.accounts.views.target_views.<a href="./src/obp_api/resources/accounts/views/target_views.py">delete</a>(view_id, \*, bank_id, account_id) -> None</code>

### UserAccountAccess

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}/user-account-access">client.accounts.views.user_account_access.<a href="./src/obp_api/resources/accounts/views/user_account_access.py">create</a>(view_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/accounts/views/user_account_access_create_params.py">params</a>) -> BinaryAPIResponse</code>

## Balances

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/balances">client.accounts.balances.<a href="./src/obp_api/resources/accounts/balances.py">retrieve</a>(account_id, \*, bank_id) -> BinaryAPIResponse</code>

## Firehose

### Transactions

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/firehose/accounts/{ACCOUNT_ID}/views/{VIEW_ID}/transactions">client.accounts.firehose.transactions.<a href="./src/obp_api/resources/accounts/firehose/transactions.py">list</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>

### Views

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/firehose/accounts/views/{VIEW_ID}">client.accounts.firehose.views.<a href="./src/obp_api/resources/accounts/firehose/views.py">list</a>(view_id, \*, bank_id) -> BinaryAPIResponse</code>

# Adapter

Methods:

- <code title="get /obp/v5.1.0/adapter">client.adapter.<a href="./src/obp_api/resources/adapter.py">retrieve</a>() -> BinaryAPIResponse</code>

# APICollections

Methods:

- <code title="post /obp/v5.1.0/my/api-collections">client.api_collections.<a href="./src/obp_api/resources/api_collections/api_collections.py">create</a>(\*\*<a href="src/obp_api/types/api_collection_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/my/api-collections/name/API_COLLECTION_NAME">client.api_collections.<a href="./src/obp_api/resources/api_collections/api_collections.py">retrieve</a>() -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/my/api-collections/API_COLLECTION_ID">client.api_collections.<a href="./src/obp_api/resources/api_collections/api_collections.py">update</a>(\*\*<a href="src/obp_api/types/api_collection_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/my/api-collections">client.api_collections.<a href="./src/obp_api/resources/api_collections/api_collections.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/my/api-collections/API_COLLECTION_ID">client.api_collections.<a href="./src/obp_api/resources/api_collections/api_collections.py">delete</a>() -> BinaryAPIResponse</code>

## APICollectionEndpoints

Methods:

- <code title="post /obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints">client.api_collections.api_collection_endpoints.<a href="./src/obp_api/resources/api_collections/api_collection_endpoints.py">create</a>(\*\*<a href="src/obp_api/types/api_collections/api_collection_endpoint_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints/OPERATION_ID">client.api_collections.api_collection_endpoints.<a href="./src/obp_api/resources/api_collections/api_collection_endpoints.py">retrieve</a>() -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/api-collections/API_COLLECTION_ID/api-collection-endpoints">client.api_collections.api_collection_endpoints.<a href="./src/obp_api/resources/api_collections/api_collection_endpoints.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/my/api-collections/API_COLLECTION_NAME/api-collection-endpoints/OPERATION_ID">client.api_collections.api_collection_endpoints.<a href="./src/obp_api/resources/api_collections/api_collection_endpoints.py">delete</a>() -> BinaryAPIResponse</code>

## Featured

Methods:

- <code title="get /obp/v5.1.0/api-collections/featured">client.api_collections.featured.<a href="./src/obp_api/resources/api_collections/featured.py">list</a>() -> BinaryAPIResponse</code>

## Sharable

Methods:

- <code title="get /obp/v5.1.0/api-collections/sharable/API_COLLECTION_ID">client.api_collections.sharable.<a href="./src/obp_api/resources/api_collections/sharable.py">retrieve</a>() -> BinaryAPIResponse</code>

## APIEndpoints

Methods:

- <code title="delete /obp/v5.1.0/my/api-collection-ids/API_COLLECTION_ID/api-collection-endpoint-ids/API_COLLECTION_ENDPOINT_ID">client.api_collections.api_endpoints.<a href="./src/obp_api/resources/api_collections/api_endpoints/api_endpoints.py">delete</a>() -> BinaryAPIResponse</code>

# API

Methods:

- <code title="get /obp/v5.1.0/root">client.api.<a href="./src/obp_api/resources/api/api.py">root</a>() -> BinaryAPIResponse</code>

## Glossary

Methods:

- <code title="get /obp/v5.1.0/api/glossary">client.api.glossary.<a href="./src/obp_api/resources/api/glossary.py">retrieve</a>() -> BinaryAPIResponse</code>

## Versions

Methods:

- <code title="get /obp/v5.1.0/api/versions">client.api.versions.<a href="./src/obp_api/resources/api/versions.py">list</a>() -> BinaryAPIResponse</code>

## SuggestedSessionTimeout

Methods:

- <code title="get /obp/v5.1.0/ui/suggested-session-timeout">client.api.suggested_session_timeout.<a href="./src/obp_api/resources/api/suggested_session_timeout.py">retrieve</a>() -> BinaryAPIResponse</code>

# Banks

Methods:

- <code title="post /obp/v5.1.0/banks">client.banks.<a href="./src/obp_api/resources/banks/banks.py">create</a>(\*\*<a href="src/obp_api/types/bank_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}">client.banks.<a href="./src/obp_api/resources/banks/banks.py">retrieve</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks">client.banks.<a href="./src/obp_api/resources/banks/banks.py">update</a>(\*\*<a href="src/obp_api/types/bank_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks">client.banks.<a href="./src/obp_api/resources/banks/banks.py">list</a>() -> BinaryAPIResponse</code>

## Customers

### Attributes

Methods:

- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/{CUSTOMER_ID}/attributes/CUSTOMER_ATTRIBUTE_ID">client.banks.customers.attributes.<a href="./src/obp_api/resources/banks/customers/attributes.py">delete</a>(customer_id, \*, bank_id) -> None</code>

## AccountApplications

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/account-applications">client.banks.account_applications.<a href="./src/obp_api/resources/banks/account_applications.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/banks/account_application_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/account-applications/{ACCOUNT_APPLICATION_ID}">client.banks.account_applications.<a href="./src/obp_api/resources/banks/account_applications.py">retrieve</a>(account_application_id, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/account-applications/{ACCOUNT_APPLICATION_ID}">client.banks.account_applications.<a href="./src/obp_api/resources/banks/account_applications.py">update</a>(account_application_id, \*, bank_id, \*\*<a href="src/obp_api/types/banks/account_application_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/account-applications">client.banks.account_applications.<a href="./src/obp_api/resources/banks/account_applications.py">list</a>(bank_id) -> BinaryAPIResponse</code>

## AccountWebHooks

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/account-web-hooks">client.banks.account_web_hooks.<a href="./src/obp_api/resources/banks/account_web_hooks.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/banks/account_web_hook_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/account-web-hooks">client.banks.account_web_hooks.<a href="./src/obp_api/resources/banks/account_web_hooks.py">update</a>(bank_id, \*\*<a href="src/obp_api/types/banks/account_web_hook_update_params.py">params</a>) -> BinaryAPIResponse</code>

## Accounts

Methods:

- <code title="put /obp/v5.1.0/management/banks/{BANK_ID}/accounts/{ACCOUNT_ID}">client.banks.accounts.<a href="./src/obp_api/resources/banks/accounts/accounts.py">update</a>(account_id, \*, bank_id, \*\*<a href="src/obp_api/types/banks/account_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts">client.banks.accounts.<a href="./src/obp_api/resources/banks/accounts/accounts.py">list</a>(bank_id) -> BinaryAPIResponse</code>

### OtherAccounts

#### PrivateAlias

Methods:

- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/private_alias">client.banks.accounts.other_accounts.private_alias.<a href="./src/obp_api/resources/banks/accounts/other_accounts/private_alias.py">delete</a>(other_account_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/banks/accounts/other_accounts/private_alias_delete_params.py">params</a>) -> BinaryAPIResponse</code>

#### PublicAlias

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/public_alias">client.banks.accounts.other_accounts.public_alias.<a href="./src/obp_api/resources/banks/accounts/other_accounts/public_alias.py">create</a>(other_account_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/banks/accounts/other_accounts/public_alias_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/public_alias">client.banks.accounts.other_accounts.public_alias.<a href="./src/obp_api/resources/banks/accounts/other_accounts/public_alias.py">retrieve</a>(other_account_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/public_alias">client.banks.accounts.other_accounts.public_alias.<a href="./src/obp_api/resources/banks/accounts/other_accounts/public_alias.py">update</a>(other_account_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/banks/accounts/other_accounts/public_alias_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/public_alias">client.banks.accounts.other_accounts.public_alias.<a href="./src/obp_api/resources/banks/accounts/other_accounts/public_alias.py">delete</a>(other_account_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/banks/accounts/other_accounts/public_alias_delete_params.py">params</a>) -> BinaryAPIResponse</code>

### StandingOrder

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/standing-order">client.banks.accounts.standing_order.<a href="./src/obp_api/resources/banks/accounts/standing_order.py">create</a>(view_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/banks/accounts/standing_order_create_params.py">params</a>) -> BinaryAPIResponse</code>

### TransactionRequestTypes

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transaction-request-types">client.banks.accounts.transaction_request_types.<a href="./src/obp_api/resources/banks/accounts/transaction_request_types.py">list</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>

### TransactionRequests

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transaction-request-types/COUNTERPARTY/transaction-requests">client.banks.accounts.transaction_requests.<a href="./src/obp_api/resources/banks/accounts/transaction_requests.py">create</a>(view_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/banks/accounts/transaction_request_create_params.py">params</a>) -> BinaryAPIResponse</code>

### Views

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views">client.banks.accounts.views.<a href="./src/obp_api/resources/banks/accounts/views/views.py">create</a>(account_id, \*, bank_id, \*\*<a href="src/obp_api/types/banks/accounts/view_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}">client.banks.accounts.views.<a href="./src/obp_api/resources/banks/accounts/views/views.py">retrieve</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}">client.banks.accounts.views.<a href="./src/obp_api/resources/banks/accounts/views/views.py">update</a>(view_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/banks/accounts/view_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views">client.banks.accounts.views.<a href="./src/obp_api/resources/banks/accounts/views/views.py">list</a>(account_id, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}">client.banks.accounts.views.<a href="./src/obp_api/resources/banks/accounts/views/views.py">delete</a>(view_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/banks/accounts/view_delete_params.py">params</a>) -> BinaryAPIResponse</code>

#### TransactionRequestTypes

##### TransactionRequests

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transaction-request-types/SIMPLE/transaction-requests">client.banks.accounts.views.transaction_request_types.transaction_requests.<a href="./src/obp_api/resources/banks/accounts/views/transaction_request_types/transaction_requests.py">create</a>(view_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/banks/accounts/views/transaction_request_types/transaction_request_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transaction-request-types/{TRANSACTION_REQUEST_TYPE}/transaction-requests/{TRANSACTION_REQUEST_ID}/challenge">client.banks.accounts.views.transaction_request_types.transaction_requests.<a href="./src/obp_api/resources/banks/accounts/views/transaction_request_types/transaction_requests.py">challenge</a>(transaction_request_id, \*, bank_id, account_id, view_id, transaction_request_type, \*\*<a href="src/obp_api/types/banks/accounts/views/transaction_request_types/transaction_request_challenge_params.py">params</a>) -> BinaryAPIResponse</code>

#### TransactionRequests

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transaction-requests/{TRANSACTION_REQUEST_ID}">client.banks.accounts.views.transaction_requests.<a href="./src/obp_api/resources/banks/accounts/views/transaction_requests.py">retrieve</a>(transaction_request_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transaction-requests">client.banks.accounts.views.transaction_requests.<a href="./src/obp_api/resources/banks/accounts/views/transaction_requests.py">list</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>

#### Transactions

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions">client.banks.accounts.views.transactions.<a href="./src/obp_api/resources/banks/accounts/views/transactions.py">list</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/double-entry-transaction">client.banks.accounts.views.transactions.<a href="./src/obp_api/resources/banks/accounts/views/transactions.py">double_entry</a>(transaction_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>

#### AccountAccess

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}/account-access/grant">client.banks.accounts.views.account_access.<a href="./src/obp_api/resources/banks/accounts/views/account_access.py">grant</a>(view_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/banks/accounts/views/account_access_grant_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/views/{VIEW_ID}/account-access/revoke">client.banks.accounts.views.account_access.<a href="./src/obp_api/resources/banks/accounts/views/account_access.py">revoke</a>(view_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/banks/accounts/views/account_access_revoke_params.py">params</a>) -> BinaryAPIResponse</code>

### Transactions

Methods:

- <code title="get /obp/v5.1.0/my/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/transactions">client.banks.accounts.transactions.<a href="./src/obp_api/resources/banks/accounts/transactions/transactions.py">list</a>(account_id, \*, bank_id) -> BinaryAPIResponse</code>

#### Attributes

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/transactions/{TRANSACTION_ID}/attributes/ATTRIBUTE_ID">client.banks.accounts.transactions.attributes.<a href="./src/obp_api/resources/banks/accounts/transactions/attributes.py">retrieve</a>(transaction_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/transactions/{TRANSACTION_ID}/attributes/{ACCOUNT_ATTRIBUTE_ID}">client.banks.accounts.transactions.attributes.<a href="./src/obp_api/resources/banks/accounts/transactions/attributes.py">update</a>(account_attribute_id, \*, bank_id, account_id, transaction_id, \*\*<a href="src/obp_api/types/banks/accounts/transactions/attribute_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/transactions/{TRANSACTION_ID}/attributes">client.banks.accounts.transactions.attributes.<a href="./src/obp_api/resources/banks/accounts/transactions/attributes.py">list</a>(transaction_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>

### Counterparties

Methods:

- <code title="post /obp/v5.1.0/management/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/counterparties">client.banks.accounts.counterparties.<a href="./src/obp_api/resources/banks/accounts/counterparties.py">create</a>(view_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/banks/accounts/counterparty_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/counterparties/{COUNTERPARTY_ID}">client.banks.accounts.counterparties.<a href="./src/obp_api/resources/banks/accounts/counterparties.py">retrieve</a>(counterparty_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/counterparties">client.banks.accounts.counterparties.<a href="./src/obp_api/resources/banks/accounts/counterparties.py">list</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/management/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/counterparties/{COUNTERPARTY_ID}">client.banks.accounts.counterparties.<a href="./src/obp_api/resources/banks/accounts/counterparties.py">delete</a>(counterparty_id, \*, bank_id, account_id, view_id) -> None</code>

### CounterpartyNames

Methods:

- <code title="get /obp/v5.1.0/management/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/counterparty-names/{COUNTERPARTY_NAME}">client.banks.accounts.counterparty_names.<a href="./src/obp_api/resources/banks/accounts/counterparty_names.py">retrieve</a>(counterparty_name, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>

### DirectDebit

Methods:

- <code title="post /obp/v5.1.0/management/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/direct-debit">client.banks.accounts.direct_debit.<a href="./src/obp_api/resources/banks/accounts/direct_debit.py">create</a>(account_id, \*, bank_id, \*\*<a href="src/obp_api/types/banks/accounts/direct_debit_create_params.py">params</a>) -> BinaryAPIResponse</code>

### Account

Methods:

- <code title="get /obp/v5.1.0/my/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/account">client.banks.accounts.account.<a href="./src/obp_api/resources/banks/accounts/account.py">retrieve</a>(account_id, \*, bank_id) -> BinaryAPIResponse</code>

## Adapter

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/adapter">client.banks.adapter.<a href="./src/obp_api/resources/banks/adapter.py">retrieve</a>(bank_id) -> BinaryAPIResponse</code>

## Atms

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/atms">client.banks.atms.<a href="./src/obp_api/resources/banks/atms/atms.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/banks/atm_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/atms/{ATM_ID}">client.banks.atms.<a href="./src/obp_api/resources/banks/atms/atms.py">retrieve</a>(atm_id, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/atms/{ATM_ID}">client.banks.atms.<a href="./src/obp_api/resources/banks/atms/atms.py">update</a>(atm_id, \*, bank_id, \*\*<a href="src/obp_api/types/banks/atm_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/atms">client.banks.atms.<a href="./src/obp_api/resources/banks/atms/atms.py">list</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/atms/{ATM_ID}">client.banks.atms.<a href="./src/obp_api/resources/banks/atms/atms.py">delete</a>(atm_id, \*, bank_id) -> None</code>

### AccessibilityFeatures

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/atms/{ATM_ID}/accessibility-features">client.banks.atms.accessibility_features.<a href="./src/obp_api/resources/banks/atms/accessibility_features.py">update</a>(atm_id, \*, bank_id, \*\*<a href="src/obp_api/types/banks/atms/accessibility_feature_update_params.py">params</a>) -> BinaryAPIResponse</code>

### Attributes

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/atms/{ATM_ID}/attributes">client.banks.atms.attributes.<a href="./src/obp_api/resources/banks/atms/attributes.py">create</a>(atm_id, \*, bank_id, \*\*<a href="src/obp_api/types/banks/atms/attribute_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/atms/{ATM_ID}/attributes/{ATM_ATTRIBUTE_ID}">client.banks.atms.attributes.<a href="./src/obp_api/resources/banks/atms/attributes.py">retrieve</a>(atm_attribute_id, \*, bank_id, atm_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/atms/{ATM_ID}/attributes/{ATM_ATTRIBUTE_ID}">client.banks.atms.attributes.<a href="./src/obp_api/resources/banks/atms/attributes.py">update</a>(atm_attribute_id, \*, bank_id, atm_id, \*\*<a href="src/obp_api/types/banks/atms/attribute_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/atms/{ATM_ID}/attributes">client.banks.atms.attributes.<a href="./src/obp_api/resources/banks/atms/attributes.py">list</a>(atm_id, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/atms/{ATM_ID}/attributes/{ATM_ATTRIBUTE_ID}">client.banks.atms.attributes.<a href="./src/obp_api/resources/banks/atms/attributes.py">delete</a>(atm_attribute_id, \*, bank_id, atm_id) -> None</code>

### LocationCategories

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/atms/{ATM_ID}/location-categories">client.banks.atms.location_categories.<a href="./src/obp_api/resources/banks/atms/location_categories.py">update</a>(atm_id, \*, bank_id, \*\*<a href="src/obp_api/types/banks/atms/location_category_update_params.py">params</a>) -> BinaryAPIResponse</code>

### Notes

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/atms/{ATM_ID}/notes">client.banks.atms.notes.<a href="./src/obp_api/resources/banks/atms/notes.py">update</a>(atm_id, \*, bank_id, \*\*<a href="src/obp_api/types/banks/atms/note_update_params.py">params</a>) -> BinaryAPIResponse</code>

### Services

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/atms/{ATM_ID}/services">client.banks.atms.services.<a href="./src/obp_api/resources/banks/atms/services.py">update</a>(atm_id, \*, bank_id, \*\*<a href="src/obp_api/types/banks/atms/service_update_params.py">params</a>) -> BinaryAPIResponse</code>

### SupportedCurrencies

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/atms/{ATM_ID}/supported-currencies">client.banks.atms.supported_currencies.<a href="./src/obp_api/resources/banks/atms/supported_currencies.py">update</a>(atm_id, \*, bank_id, \*\*<a href="src/obp_api/types/banks/atms/supported_currency_update_params.py">params</a>) -> BinaryAPIResponse</code>

### SupportedLanguages

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/atms/{ATM_ID}/supported-languages">client.banks.atms.supported_languages.<a href="./src/obp_api/resources/banks/atms/supported_languages.py">update</a>(atm_id, \*, bank_id, \*\*<a href="src/obp_api/types/banks/atms/supported_language_update_params.py">params</a>) -> BinaryAPIResponse</code>

## Attributes

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/attribute">client.banks.attributes.<a href="./src/obp_api/resources/banks/attributes.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/banks/attribute_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/attributes/BANK_ATTRIBUTE_ID">client.banks.attributes.<a href="./src/obp_api/resources/banks/attributes.py">retrieve</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/attributes/BANK_ATTRIBUTE_ID">client.banks.attributes.<a href="./src/obp_api/resources/banks/attributes.py">update</a>(bank_id, \*\*<a href="src/obp_api/types/banks/attribute_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/attributes">client.banks.attributes.<a href="./src/obp_api/resources/banks/attributes.py">list</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/attributes/BANK_ATTRIBUTE_ID">client.banks.attributes.<a href="./src/obp_api/resources/banks/attributes.py">delete</a>(bank_id) -> None</code>

## AttributeDefinitions

### Accounts

Methods:

- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/ATTRIBUTE_DEFINITION_ID/account">client.banks.attribute_definitions.accounts.<a href="./src/obp_api/resources/banks/attribute_definitions/accounts.py">retrieve</a>(bank_id) -> None</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/ATTRIBUTE_DEFINITION_ID/card">client.banks.attribute_definitions.accounts.<a href="./src/obp_api/resources/banks/attribute_definitions/accounts.py">update</a>(bank_id) -> None</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/ATTRIBUTE_DEFINITION_ID/customer">client.banks.attribute_definitions.accounts.<a href="./src/obp_api/resources/banks/attribute_definitions/accounts.py">delete</a>(bank_id) -> None</code>

### Cards

Methods:

- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/ATTRIBUTE_DEFINITION_ID/product">client.banks.attribute_definitions.cards.<a href="./src/obp_api/resources/banks/attribute_definitions/cards.py">delete</a>(bank_id) -> None</code>

### Customers

Methods:

- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/ATTRIBUTE_DEFINITION_ID/transaction">client.banks.attribute_definitions.customers.<a href="./src/obp_api/resources/banks/attribute_definitions/customers.py">delete</a>(bank_id) -> None</code>

### Products

Methods:

- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/ATTRIBUTE_DEFINITION_ID/transaction-request">client.banks.attribute_definitions.products.<a href="./src/obp_api/resources/banks/attribute_definitions/products.py">delete</a>(bank_id) -> BinaryAPIResponse</code>

### Transactions

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/account">client.banks.attribute_definitions.transactions.<a href="./src/obp_api/resources/banks/attribute_definitions/transactions.py">delete</a>(bank_id) -> BinaryAPIResponse</code>

### TransactionRequests

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/transaction-request">client.banks.attribute_definitions.transaction_requests.<a href="./src/obp_api/resources/banks/attribute_definitions/transaction_requests.py">retrieve</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/transaction-request">client.banks.attribute_definitions.transaction_requests.<a href="./src/obp_api/resources/banks/attribute_definitions/transaction_requests.py">update</a>(bank_id, \*\*<a href="src/obp_api/types/banks/attribute_definitions/transaction_request_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/account">client.banks.attribute_definitions.transaction_requests.<a href="./src/obp_api/resources/banks/attribute_definitions/transaction_requests.py">delete</a>(bank_id, \*\*<a href="src/obp_api/types/banks/attribute_definitions/transaction_request_delete_params.py">params</a>) -> BinaryAPIResponse</code>

### Banks

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/bank">client.banks.attribute_definitions.banks.<a href="./src/obp_api/resources/banks/attribute_definitions/banks.py">update</a>(bank_id, \*\*<a href="src/obp_api/types/banks/attribute_definitions/bank_update_params.py">params</a>) -> BinaryAPIResponse</code>

### Card

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/card">client.banks.attribute_definitions.card.<a href="./src/obp_api/resources/banks/attribute_definitions/card.py">retrieve</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/card">client.banks.attribute_definitions.card.<a href="./src/obp_api/resources/banks/attribute_definitions/card.py">update</a>(bank_id, \*\*<a href="src/obp_api/types/banks/attribute_definitions/card_update_params.py">params</a>) -> BinaryAPIResponse</code>

### Customer

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/customer">client.banks.attribute_definitions.customer.<a href="./src/obp_api/resources/banks/attribute_definitions/customer.py">retrieve</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/customer">client.banks.attribute_definitions.customer.<a href="./src/obp_api/resources/banks/attribute_definitions/customer.py">update</a>(bank_id, \*\*<a href="src/obp_api/types/banks/attribute_definitions/customer_update_params.py">params</a>) -> BinaryAPIResponse</code>

### Product

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/product">client.banks.attribute_definitions.product.<a href="./src/obp_api/resources/banks/attribute_definitions/product.py">retrieve</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/product">client.banks.attribute_definitions.product.<a href="./src/obp_api/resources/banks/attribute_definitions/product.py">update</a>(bank_id, \*\*<a href="src/obp_api/types/banks/attribute_definitions/product_update_params.py">params</a>) -> BinaryAPIResponse</code>

### Transaction

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/transaction">client.banks.attribute_definitions.transaction.<a href="./src/obp_api/resources/banks/attribute_definitions/transaction.py">retrieve</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/attribute-definitions/transaction">client.banks.attribute_definitions.transaction.<a href="./src/obp_api/resources/banks/attribute_definitions/transaction.py">update</a>(bank_id, \*\*<a href="src/obp_api/types/banks/attribute_definitions/transaction_update_params.py">params</a>) -> BinaryAPIResponse</code>

## Balances

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/balances">client.banks.balances.<a href="./src/obp_api/resources/banks/balances.py">list</a>(bank_id) -> BinaryAPIResponse</code>

## Branches

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/branches">client.banks.branches.<a href="./src/obp_api/resources/banks/branches.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/banks/branch_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/branches/{BRANCH_ID}">client.banks.branches.<a href="./src/obp_api/resources/banks/branches.py">retrieve</a>(branch_id, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/branches">client.banks.branches.<a href="./src/obp_api/resources/banks/branches.py">list</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/branches/{BRANCH_ID}">client.banks.branches.<a href="./src/obp_api/resources/banks/branches.py">delete</a>(branch_id, \*, bank_id) -> None</code>

## Consents

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/consents/{CONSENT_ID}">client.banks.consents.<a href="./src/obp_api/resources/banks/consents.py">update</a>(consent_id, \*, bank_id, \*\*<a href="src/obp_api/types/banks/consent_update_params.py">params</a>) -> BinaryAPIResponse</code>

## Entitlements

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/entitlements">client.banks.entitlements.<a href="./src/obp_api/resources/banks/entitlements.py">list</a>(bank_id) -> BinaryAPIResponse</code>

## FirehoseCustomers

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/firehose/customers">client.banks.firehose_customers.<a href="./src/obp_api/resources/banks/firehose_customers.py">list</a>(bank_id) -> BinaryAPIResponse</code>

## Fx

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/fx/{FROM_CURRENCY_CODE}/{TO_CURRENCY_CODE}">client.banks.fx.<a href="./src/obp_api/resources/banks/fx.py">retrieve</a>(to_currency_code, \*, bank_id, from_currency_code) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/fx">client.banks.fx.<a href="./src/obp_api/resources/banks/fx.py">update</a>(bank_id, \*\*<a href="src/obp_api/types/banks/fx_update_params.py">params</a>) -> BinaryAPIResponse</code>

## Management

### Historical

#### Transactions

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/management/historical/transactions">client.banks.management.historical.transactions.<a href="./src/obp_api/resources/banks/management/historical/transactions.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/banks/management/historical/transaction_create_params.py">params</a>) -> BinaryAPIResponse</code>

## Meetings

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/meetings">client.banks.meetings.<a href="./src/obp_api/resources/banks/meetings.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/banks/meeting_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/meetings/{MEETING_ID}">client.banks.meetings.<a href="./src/obp_api/resources/banks/meetings.py">retrieve</a>(meeting_id, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/meetings">client.banks.meetings.<a href="./src/obp_api/resources/banks/meetings.py">list</a>(bank_id) -> BinaryAPIResponse</code>

## MyConsentInfos

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/my/consent-infos">client.banks.my_consent_infos.<a href="./src/obp_api/resources/banks/my_consent_infos.py">list</a>(bank_id) -> BinaryAPIResponse</code>

## MyConsents

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/my/consents">client.banks.my_consents.<a href="./src/obp_api/resources/banks/my_consents.py">list</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/my/consents/{CONSENT_ID}/revoke">client.banks.my_consents.<a href="./src/obp_api/resources/banks/my_consents.py">revoke</a>(consent_id, \*, bank_id) -> BinaryAPIResponse</code>

## Webhooks

Methods:

- <code title="get /obp/v5.1.0/management/banks/{BANK_ID}/account-web-hooks">client.banks.webhooks.<a href="./src/obp_api/resources/banks/webhooks.py">list</a>(bank_id) -> BinaryAPIResponse</code>

## DynamicEndpoints

Methods:

- <code title="get /obp/v5.1.0/management/banks/{BANK_ID}/dynamic-endpoints/DYNAMIC_ENDPOINT_ID">client.banks.dynamic_endpoints.<a href="./src/obp_api/resources/banks/dynamic_endpoints/dynamic_endpoints.py">retrieve</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/management/banks/{BANK_ID}/dynamic-endpoints/DYNAMIC_ENDPOINT_ID">client.banks.dynamic_endpoints.<a href="./src/obp_api/resources/banks/dynamic_endpoints/dynamic_endpoints.py">delete</a>(bank_id) -> None</code>

### Host

Methods:

- <code title="put /obp/v5.1.0/management/banks/{BANK_ID}/dynamic-endpoints/DYNAMIC_ENDPOINT_ID/host">client.banks.dynamic_endpoints.host.<a href="./src/obp_api/resources/banks/dynamic_endpoints/host.py">update</a>(bank_id, \*\*<a href="src/obp_api/types/banks/dynamic_endpoints/host_update_params.py">params</a>) -> BinaryAPIResponse</code>

## DynamicEntities

Methods:

- <code title="post /obp/v5.1.0/management/banks/{BANK_ID}/dynamic-entities">client.banks.dynamic_entities.<a href="./src/obp_api/resources/banks/dynamic_entities.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/banks/dynamic_entity_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/management/banks/{BANK_ID}/dynamic-entities/{DYNAMIC_ENTITY_ID}">client.banks.dynamic_entities.<a href="./src/obp_api/resources/banks/dynamic_entities.py">update</a>(dynamic_entity_id, \*, bank_id, \*\*<a href="src/obp_api/types/banks/dynamic_entity_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/banks/{BANK_ID}/dynamic-entities">client.banks.dynamic_entities.<a href="./src/obp_api/resources/banks/dynamic_entities.py">list</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/management/banks/{BANK_ID}/dynamic-entities/{DYNAMIC_ENTITY_ID}">client.banks.dynamic_entities.<a href="./src/obp_api/resources/banks/dynamic_entities.py">delete</a>(dynamic_entity_id, \*, bank_id) -> None</code>

## DynamicMessageDocs

Methods:

- <code title="post /obp/v5.1.0/management/banks/{BANK_ID}/dynamic-message-docs">client.banks.dynamic_message_docs.<a href="./src/obp_api/resources/banks/dynamic_message_docs.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/banks/dynamic_message_doc_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/banks/{BANK_ID}/dynamic-message-docs/DYNAMIC_MESSAGE_DOC_ID">client.banks.dynamic_message_docs.<a href="./src/obp_api/resources/banks/dynamic_message_docs.py">retrieve</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/banks/{BANK_ID}/dynamic-message-docs">client.banks.dynamic_message_docs.<a href="./src/obp_api/resources/banks/dynamic_message_docs.py">list</a>(bank_id) -> BinaryAPIResponse</code>

# AccountsHeld

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts-held">client.accounts_held.<a href="./src/obp_api/resources/accounts_held.py">list</a>(bank_id) -> BinaryAPIResponse</code>

# Counterparties

## Metadata

### OpenCorporatesURL

Methods:

- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/metadata/open_corporates_url">client.counterparties.metadata.open_corporates_url.<a href="./src/obp_api/resources/counterparties/metadata/open_corporates_url.py">delete</a>(other_account_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/counterparties/metadata/open_corporates_url_delete_params.py">params</a>) -> BinaryAPIResponse</code>

### PhysicalLocation

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/metadata/physical_location">client.counterparties.metadata.physical_location.<a href="./src/obp_api/resources/counterparties/metadata/physical_location.py">create</a>(other_account_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/counterparties/metadata/physical_location_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/metadata/physical_location">client.counterparties.metadata.physical_location.<a href="./src/obp_api/resources/counterparties/metadata/physical_location.py">update</a>(other_account_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/counterparties/metadata/physical_location_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/metadata/physical_location">client.counterparties.metadata.physical_location.<a href="./src/obp_api/resources/counterparties/metadata/physical_location.py">delete</a>(other_account_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/counterparties/metadata/physical_location_delete_params.py">params</a>) -> BinaryAPIResponse</code>

### URL

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/metadata/url">client.counterparties.metadata.url.<a href="./src/obp_api/resources/counterparties/metadata/url.py">create</a>(other_account_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/counterparties/metadata/url_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/metadata/url">client.counterparties.metadata.url.<a href="./src/obp_api/resources/counterparties/metadata/url.py">update</a>(other_account_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/counterparties/metadata/url_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/metadata/url">client.counterparties.metadata.url.<a href="./src/obp_api/resources/counterparties/metadata/url.py">delete</a>(other_account_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/counterparties/metadata/url_delete_params.py">params</a>) -> BinaryAPIResponse</code>

## PrivateAlias

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/private_alias">client.counterparties.private_alias.<a href="./src/obp_api/resources/counterparties/private_alias.py">create</a>(other_account_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/counterparties/private_alias_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/private_alias">client.counterparties.private_alias.<a href="./src/obp_api/resources/counterparties/private_alias.py">retrieve</a>(other_account_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/other_accounts/{OTHER_ACCOUNT_ID}/private_alias">client.counterparties.private_alias.<a href="./src/obp_api/resources/counterparties/private_alias.py">update</a>(other_account_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/counterparties/private_alias_update_params.py">params</a>) -> BinaryAPIResponse</code>

# Transactions

## Metadata

### Comments

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/comments">client.transactions.metadata.comments.<a href="./src/obp_api/resources/transactions/metadata/comments.py">create</a>(transaction_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/transactions/metadata/comment_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/comments">client.transactions.metadata.comments.<a href="./src/obp_api/resources/transactions/metadata/comments.py">list</a>(transaction_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/comments/{COMMENT_ID}">client.transactions.metadata.comments.<a href="./src/obp_api/resources/transactions/metadata/comments.py">delete</a>(comment_id, \*, bank_id, account_id, view_id, transaction_id, \*\*<a href="src/obp_api/types/transactions/metadata/comment_delete_params.py">params</a>) -> BinaryAPIResponse</code>

### Images

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/images">client.transactions.metadata.images.<a href="./src/obp_api/resources/transactions/metadata/images.py">create</a>(transaction_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/transactions/metadata/image_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/images">client.transactions.metadata.images.<a href="./src/obp_api/resources/transactions/metadata/images.py">list</a>(transaction_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/images/{IMAGE_ID}">client.transactions.metadata.images.<a href="./src/obp_api/resources/transactions/metadata/images.py">delete</a>(image_id, \*, bank_id, account_id, view_id, transaction_id, \*\*<a href="src/obp_api/types/transactions/metadata/image_delete_params.py">params</a>) -> BinaryAPIResponse</code>

### Narrative

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/narrative">client.transactions.metadata.narrative.<a href="./src/obp_api/resources/transactions/metadata/narrative.py">create</a>(transaction_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/transactions/metadata/narrative_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/narrative">client.transactions.metadata.narrative.<a href="./src/obp_api/resources/transactions/metadata/narrative.py">retrieve</a>(transaction_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/narrative">client.transactions.metadata.narrative.<a href="./src/obp_api/resources/transactions/metadata/narrative.py">update</a>(transaction_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/transactions/metadata/narrative_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/narrative">client.transactions.metadata.narrative.<a href="./src/obp_api/resources/transactions/metadata/narrative.py">delete</a>(transaction_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/transactions/metadata/narrative_delete_params.py">params</a>) -> BinaryAPIResponse</code>

### Tags

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/tags">client.transactions.metadata.tags.<a href="./src/obp_api/resources/transactions/metadata/tags.py">create</a>(transaction_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/transactions/metadata/tag_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/tags">client.transactions.metadata.tags.<a href="./src/obp_api/resources/transactions/metadata/tags.py">list</a>(transaction_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/tags/{TAG_ID}">client.transactions.metadata.tags.<a href="./src/obp_api/resources/transactions/metadata/tags.py">delete</a>(tag_id, \*, bank_id, account_id, view_id, transaction_id, \*\*<a href="src/obp_api/types/transactions/metadata/tag_delete_params.py">params</a>) -> BinaryAPIResponse</code>

### Where

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/where">client.transactions.metadata.where.<a href="./src/obp_api/resources/transactions/metadata/where.py">create</a>(transaction_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/transactions/metadata/where_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/where">client.transactions.metadata.where.<a href="./src/obp_api/resources/transactions/metadata/where.py">retrieve</a>(transaction_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/where">client.transactions.metadata.where.<a href="./src/obp_api/resources/transactions/metadata/where.py">update</a>(transaction_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/transactions/metadata/where_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/metadata/where">client.transactions.metadata.where.<a href="./src/obp_api/resources/transactions/metadata/where.py">delete</a>(transaction_id, \*, bank_id, account_id, view_id, \*\*<a href="src/obp_api/types/transactions/metadata/where_delete_params.py">params</a>) -> BinaryAPIResponse</code>

## OtherAccount

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/other_account">client.transactions.other_account.<a href="./src/obp_api/resources/transactions/other_account.py">retrieve</a>(transaction_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>

## Transaction

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/{VIEW_ID}/transactions/{TRANSACTION_ID}/transaction">client.transactions.transaction.<a href="./src/obp_api/resources/transactions/transaction.py">retrieve</a>(transaction_id, \*, bank_id, account_id, view_id) -> BinaryAPIResponse</code>

## TransactionAttributes

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/transactions/{TRANSACTION_ID}/attribute">client.transactions.transaction_attributes.<a href="./src/obp_api/resources/transactions/transaction_attributes.py">create</a>(transaction_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/transactions/transaction_attribute_create_params.py">params</a>) -> BinaryAPIResponse</code>

## BalancingTransaction

Methods:

- <code title="get /obp/v5.1.0/transactions/{TRANSACTION_ID}/balancing-transaction">client.transactions.balancing_transaction.<a href="./src/obp_api/resources/transactions/balancing_transaction.py">retrieve</a>(transaction_id) -> BinaryAPIResponse</code>

# CustomerAccountLinks

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/customer-account-links">client.customer_account_links.<a href="./src/obp_api/resources/customer_account_links.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/customer_account_link_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID">client.customer_account_links.<a href="./src/obp_api/resources/customer_account_links.py">retrieve</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID">client.customer_account_links.<a href="./src/obp_api/resources/customer_account_links.py">update</a>(bank_id, \*\*<a href="src/obp_api/types/customer_account_link_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/customer-account-links">client.customer_account_links.<a href="./src/obp_api/resources/customer_account_links.py">list</a>(account_id, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/customer-account-links/CUSTOMER_ACCOUNT_LINK_ID">client.customer_account_links.<a href="./src/obp_api/resources/customer_account_links.py">delete</a>(bank_id) -> None</code>

# Permissions

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/permissions/{PROVIDER}/{PROVIDER_ID}">client.permissions.<a href="./src/obp_api/resources/permissions.py">retrieve</a>(provider_id, \*, bank_id, account_id, provider) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/permissions">client.permissions.<a href="./src/obp_api/resources/permissions.py">list</a>(account_id, \*, bank_id) -> BinaryAPIResponse</code>

# AccountProducts

## Attributes

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/products/{PRODUCT_CODE}/attribute">client.account_products.attributes.<a href="./src/obp_api/resources/account_products/attributes.py">create</a>(product_code, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/account_products/attribute_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/products/{PRODUCT_CODE}/attributes/{ACCOUNT_ATTRIBUTE_ID}">client.account_products.attributes.<a href="./src/obp_api/resources/account_products/attributes.py">update</a>(account_attribute_id, \*, bank_id, account_id, product_code, \*\*<a href="src/obp_api/types/account_products/attribute_update_params.py">params</a>) -> BinaryAPIResponse</code>

# TransactionRequests

Methods:

- <code title="post /obp/v5.1.0/transaction-request-types/CARD/transaction-requests">client.transaction_requests.<a href="./src/obp_api/resources/transaction_requests/transaction_requests.py">create</a>(\*\*<a href="src/obp_api/types/transaction_request_create_params.py">params</a>) -> BinaryAPIResponse</code>

## TransactionRequestAttributes

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/transaction-requests/{TRANSACTION_REQUEST_ID}/attribute">client.transaction_requests.transaction_request_attributes.<a href="./src/obp_api/resources/transaction_requests/transaction_request_attributes.py">create</a>(transaction_request_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/transaction_requests/transaction_request_attribute_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/transaction-requests/{TRANSACTION_REQUEST_ID}/attributes/ATTRIBUTE_ID">client.transaction_requests.transaction_request_attributes.<a href="./src/obp_api/resources/transaction_requests/transaction_request_attributes.py">retrieve</a>(transaction_request_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/transaction-requests/{TRANSACTION_REQUEST_ID}/attributes/ATTRIBUTE_ID">client.transaction_requests.transaction_request_attributes.<a href="./src/obp_api/resources/transaction_requests/transaction_request_attributes.py">update</a>(transaction_request_id, \*, bank_id, account_id, \*\*<a href="src/obp_api/types/transaction_requests/transaction_request_attribute_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/transaction-requests/{TRANSACTION_REQUEST_ID}/attributes">client.transaction_requests.transaction_request_attributes.<a href="./src/obp_api/resources/transaction_requests/transaction_request_attributes.py">list</a>(transaction_request_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>

# BankAccounts

## AccountIDs

### Private

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/account_ids/private">client.bank_accounts.account_ids.private.<a href="./src/obp_api/resources/bank_accounts/account_ids/private.py">list</a>(bank_id) -> BinaryAPIResponse</code>

## Private

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/private">client.bank_accounts.private.<a href="./src/obp_api/resources/bank_accounts/private.py">list</a>(bank_id) -> BinaryAPIResponse</code>

## Public

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/accounts/public">client.bank_accounts.public.<a href="./src/obp_api/resources/bank_accounts/public.py">list</a>(bank_id) -> BinaryAPIResponse</code>

# Consents

Methods:

- <code title="get /obp/v5.1.0/consumer/current/consents/{CONSENT_ID}">client.consents.<a href="./src/obp_api/resources/consents/consents.py">retrieve</a>(consent_id) -> BinaryAPIResponse</code>
- <code title="post /obp/v5.1.0/banks/{BANK_ID}/consents/{CONSENT_ID}/challenge">client.consents.<a href="./src/obp_api/resources/consents/consents.py">challenge</a>(consent_id, \*, bank_id, \*\*<a href="src/obp_api/types/consent_challenge_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/consents/{CONSENT_ID}">client.consents.<a href="./src/obp_api/resources/consents/consents.py">revoke</a>(consent_id, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/consents/{CONSENT_ID}/user-update-request">client.consents.<a href="./src/obp_api/resources/consents/consents.py">user_update_request</a>(consent_id, \*, bank_id, \*\*<a href="src/obp_api/types/consent_user_update_request_params.py">params</a>) -> BinaryAPIResponse</code>

## Email

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/my/consents/EMAIL">client.consents.email.<a href="./src/obp_api/resources/consents/email.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/consents/email_create_params.py">params</a>) -> BinaryAPIResponse</code>

## Implicit

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/my/consents/IMPLICIT">client.consents.implicit.<a href="./src/obp_api/resources/consents/implicit.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/consents/implicit_create_params.py">params</a>) -> BinaryAPIResponse</code>

## SMS

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/my/consents/SMS">client.consents.sms.<a href="./src/obp_api/resources/consents/sms.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/consents/sms_create_params.py">params</a>) -> BinaryAPIResponse</code>

# CRMEvents

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/crm-events">client.crm_events.<a href="./src/obp_api/resources/crm_events.py">list</a>(bank_id) -> BinaryAPIResponse</code>

# Currencies

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/currencies">client.currencies.<a href="./src/obp_api/resources/currencies.py">list</a>(bank_id) -> BinaryAPIResponse</code>

# Customers

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/customers">client.customers.<a href="./src/obp_api/resources/customers/customers.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/customer_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}">client.customers.<a href="./src/obp_api/resources/customers/customers.py">retrieve</a>(customer_id, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/my/customers">client.customers.<a href="./src/obp_api/resources/customers/customers.py">list</a>() -> BinaryAPIResponse</code>

## Messages

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/messages">client.customers.messages.<a href="./src/obp_api/resources/customers/messages.py">create</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/message_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/messages">client.customers.messages.<a href="./src/obp_api/resources/customers/messages.py">list</a>(customer_id, \*, bank_id) -> BinaryAPIResponse</code>

## Minimal

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/customers-minimal">client.customers.minimal.<a href="./src/obp_api/resources/customers/minimal.py">list</a>(bank_id) -> BinaryAPIResponse</code>

## Addresses

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/address">client.customers.addresses.<a href="./src/obp_api/resources/customers/addresses.py">create</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/address_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/addresses/{CUSTOMER_ADDRESS_ID}">client.customers.addresses.<a href="./src/obp_api/resources/customers/addresses.py">update</a>(customer_address_id, \*, bank_id, customer_id, \*\*<a href="src/obp_api/types/customers/address_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/addresses">client.customers.addresses.<a href="./src/obp_api/resources/customers/addresses.py">list</a>(customer_id, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/addresses/{CUSTOMER_ADDRESS_ID}">client.customers.addresses.<a href="./src/obp_api/resources/customers/addresses.py">delete</a>(customer_address_id, \*, bank_id, customer_id) -> None</code>

## Attribute

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/attribute">client.customers.attribute.<a href="./src/obp_api/resources/customers/attribute.py">create</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/attribute_create_params.py">params</a>) -> BinaryAPIResponse</code>

## Attributes

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/attributes/ATTRIBUTE_ID">client.customers.attributes.<a href="./src/obp_api/resources/customers/attributes.py">retrieve</a>(customer_id, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/attributes/CUSTOMER_ATTRIBUTE_ID">client.customers.attributes.<a href="./src/obp_api/resources/customers/attributes.py">update</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/attribute_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/attributes">client.customers.attributes.<a href="./src/obp_api/resources/customers/attributes.py">list</a>(customer_id, \*, bank_id) -> BinaryAPIResponse</code>

## Branch

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/branch">client.customers.branch.<a href="./src/obp_api/resources/customers/branch.py">update</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/branch_update_params.py">params</a>) -> BinaryAPIResponse</code>

## CorrelatedUsers

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/correlated-users">client.customers.correlated_users.<a href="./src/obp_api/resources/customers/correlated_users.py">list</a>(customer_id, \*, bank_id) -> BinaryAPIResponse</code>

## CreditLimit

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/credit-limit">client.customers.credit_limit.<a href="./src/obp_api/resources/customers/credit_limit.py">update</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/credit_limit_update_params.py">params</a>) -> BinaryAPIResponse</code>

## CreditRatingAndSource

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/credit-rating-and-source">client.customers.credit_rating_and_source.<a href="./src/obp_api/resources/customers/credit_rating_and_source.py">update</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/credit_rating_and_source_update_params.py">params</a>) -> BinaryAPIResponse</code>

## CustomerAccountLinks

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/customer-account-links">client.customers.customer_account_links.<a href="./src/obp_api/resources/customers/customer_account_links.py">list</a>(customer_id, \*, bank_id) -> BinaryAPIResponse</code>

## Data

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/data">client.customers.data.<a href="./src/obp_api/resources/customers/data.py">update</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/data_update_params.py">params</a>) -> BinaryAPIResponse</code>

## Email

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/email">client.customers.email.<a href="./src/obp_api/resources/customers/email.py">update</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/email_update_params.py">params</a>) -> BinaryAPIResponse</code>

## Identity

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/identity">client.customers.identity.<a href="./src/obp_api/resources/customers/identity.py">update</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/identity_update_params.py">params</a>) -> BinaryAPIResponse</code>

## KYCChecks

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/kyc_check/{KYC_CHECK_ID}">client.customers.kyc_checks.<a href="./src/obp_api/resources/customers/kyc_checks.py">update</a>(kyc_check_id, \*, bank_id, customer_id, \*\*<a href="src/obp_api/types/customers/kyc_check_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/customers/{CUSTOMER_ID}/kyc_checks">client.customers.kyc_checks.<a href="./src/obp_api/resources/customers/kyc_checks.py">list</a>(customer_id) -> BinaryAPIResponse</code>

## KYCDocuments

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/kyc_documents/{KYC_DOCUMENT_ID}">client.customers.kyc_documents.<a href="./src/obp_api/resources/customers/kyc_documents.py">update</a>(kyc_document_id, \*, bank_id, customer_id, \*\*<a href="src/obp_api/types/customers/kyc_document_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/customers/{CUSTOMER_ID}/kyc_documents">client.customers.kyc_documents.<a href="./src/obp_api/resources/customers/kyc_documents.py">list</a>(customer_id) -> BinaryAPIResponse</code>

## KYCMedia

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/kyc_media/{KYC_MEDIA_ID}">client.customers.kyc_media.<a href="./src/obp_api/resources/customers/kyc_media.py">update</a>(kyc_media_id, \*, bank_id, customer_id, \*\*<a href="src/obp_api/types/customers/kyc_media_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/customers/{CUSTOMER_ID}/kyc_media">client.customers.kyc_media.<a href="./src/obp_api/resources/customers/kyc_media.py">list</a>(customer_id) -> BinaryAPIResponse</code>

## KYCStatuses

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/kyc_statuses">client.customers.kyc_statuses.<a href="./src/obp_api/resources/customers/kyc_statuses.py">update</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/kyc_status_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/customers/{CUSTOMER_ID}/kyc_statuses">client.customers.kyc_statuses.<a href="./src/obp_api/resources/customers/kyc_statuses.py">list</a>(customer_id) -> BinaryAPIResponse</code>

## MobileNumber

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/mobile-number">client.customers.mobile_number.<a href="./src/obp_api/resources/customers/mobile_number.py">update</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/mobile_number_update_params.py">params</a>) -> BinaryAPIResponse</code>

## Number

Methods:

- <code title="put /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/number">client.customers.number.<a href="./src/obp_api/resources/customers/number.py">update</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/number_update_params.py">params</a>) -> BinaryAPIResponse</code>

## SocialMediaHandles

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/social_media_handles">client.customers.social_media_handles.<a href="./src/obp_api/resources/customers/social_media_handles.py">create</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/social_media_handle_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/social_media_handles">client.customers.social_media_handles.<a href="./src/obp_api/resources/customers/social_media_handles.py">list</a>(customer_id, \*, bank_id) -> BinaryAPIResponse</code>

## TaxResidences

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/tax-residence">client.customers.tax_residences.<a href="./src/obp_api/resources/customers/tax_residences.py">create</a>(customer_id, \*, bank_id, \*\*<a href="src/obp_api/types/customers/tax_residence_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/tax-residences">client.customers.tax_residences.<a href="./src/obp_api/resources/customers/tax_residences.py">list</a>(customer_id, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/customers/{CUSTOMER_ID}/tax_residencies/{TAX_RESIDENCE_ID}">client.customers.tax_residences.<a href="./src/obp_api/resources/customers/tax_residences.py">delete</a>(tax_residence_id, \*, bank_id, customer_id) -> None</code>

## CustomerNumber

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/customers/customer-number">client.customers.customer_number.<a href="./src/obp_api/resources/customers/customer_number.py">retrieve</a>(bank_id, \*\*<a href="src/obp_api/types/customers/customer_number_retrieve_params.py">params</a>) -> BinaryAPIResponse</code>

## CustomerNumberQuery

### Overview

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/customers/customer-number-query/overview">client.customers.customer_number_query.overview.<a href="./src/obp_api/resources/customers/customer_number_query/overview.py">retrieve</a>(bank_id, \*\*<a href="src/obp_api/types/customers/customer_number_query/overview_retrieve_params.py">params</a>) -> BinaryAPIResponse</code>

### OverviewFlat

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/customers/customer-number-query/overview-flat">client.customers.customer_number_query.overview_flat.<a href="./src/obp_api/resources/customers/customer_number_query/overview_flat.py">retrieve</a>(bank_id, \*\*<a href="src/obp_api/types/customers/customer_number_query/overview_flat_retrieve_params.py">params</a>) -> BinaryAPIResponse</code>

## AccountsMinimal

Methods:

- <code title="get /obp/v5.1.0/customers/{CUSTOMER_ID}/accounts-minimal">client.customers.accounts_minimal.<a href="./src/obp_api/resources/customers/accounts_minimal.py">list</a>(customer_id) -> BinaryAPIResponse</code>

## Cascade

Methods:

- <code title="delete /obp/v5.1.0/management/cascading/banks/{BANK_ID}/customers/{CUSTOMER_ID}">client.customers.cascade.<a href="./src/obp_api/resources/customers/cascade.py">delete</a>(customer_id, \*, bank_id) -> None</code>

# ProductCollections

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/product-collections/{COLLECTION_CODE}">client.product_collections.<a href="./src/obp_api/resources/product_collections.py">retrieve</a>(collection_code, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/product-collections/{COLLECTION_CODE}">client.product_collections.<a href="./src/obp_api/resources/product_collections.py">update</a>(collection_code, \*, bank_id, \*\*<a href="src/obp_api/types/product_collection_update_params.py">params</a>) -> BinaryAPIResponse</code>

# ProductTree

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/product-tree/{PRODUCT_CODE}">client.product_tree.<a href="./src/obp_api/resources/product_tree.py">retrieve</a>(product_code, \*, bank_id) -> BinaryAPIResponse</code>

# Products

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/products/{PRODUCT_CODE}">client.products.<a href="./src/obp_api/resources/products/products.py">retrieve</a>(product_code, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/products/{PRODUCT_CODE}">client.products.<a href="./src/obp_api/resources/products/products.py">update</a>(product_code, \*, bank_id, \*\*<a href="src/obp_api/types/product_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/products">client.products.<a href="./src/obp_api/resources/products/products.py">list</a>(bank_id) -> BinaryAPIResponse</code>

## Attributes

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/products/{PRODUCT_CODE}/attribute">client.products.attributes.<a href="./src/obp_api/resources/products/attributes.py">create</a>(product_code, \*, bank_id, \*\*<a href="src/obp_api/types/products/attribute_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/products/{PRODUCT_CODE}/attributes/{PRODUCT_ATTRIBUTE_ID}">client.products.attributes.<a href="./src/obp_api/resources/products/attributes.py">retrieve</a>(product_attribute_id, \*, bank_id, product_code) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/products/{PRODUCT_CODE}/attributes/{PRODUCT_ATTRIBUTE_ID}">client.products.attributes.<a href="./src/obp_api/resources/products/attributes.py">update</a>(product_attribute_id, \*, bank_id, product_code, \*\*<a href="src/obp_api/types/products/attribute_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/products/{PRODUCT_CODE}/attributes/{PRODUCT_ATTRIBUTE_ID}">client.products.attributes.<a href="./src/obp_api/resources/products/attributes.py">delete</a>(product_attribute_id, \*, bank_id, product_code) -> None</code>

## Fees

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/products/{PRODUCT_CODE}/fee">client.products.fees.<a href="./src/obp_api/resources/products/fees.py">create</a>(product_code, \*, bank_id, \*\*<a href="src/obp_api/types/products/fee_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/products/{PRODUCT_CODE}/fees/PRODUCT_FEE_ID">client.products.fees.<a href="./src/obp_api/resources/products/fees.py">retrieve</a>(product_code, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/banks/{BANK_ID}/products/{PRODUCT_CODE}/fees/PRODUCT_FEE_ID">client.products.fees.<a href="./src/obp_api/resources/products/fees.py">update</a>(product_code, \*, bank_id, \*\*<a href="src/obp_api/types/products/fee_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/banks/{BANK_ID}/products/{PRODUCT_CODE}/fees">client.products.fees.<a href="./src/obp_api/resources/products/fees.py">list</a>(product_code, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/products/{PRODUCT_CODE}/fees/PRODUCT_FEE_ID">client.products.fees.<a href="./src/obp_api/resources/products/fees.py">delete</a>(product_code, \*, bank_id) -> BinaryAPIResponse</code>

## Cascade

Methods:

- <code title="delete /obp/v5.1.0/management/cascading/banks/{BANK_ID}/products/{PRODUCT_CODE}">client.products.cascade.<a href="./src/obp_api/resources/products/cascade.py">delete</a>(product_code, \*, bank_id) -> None</code>

# PublicAccounts

## Account

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/public/accounts/{ACCOUNT_ID}/{VIEW_ID}/account">client.public_accounts.account.<a href="./src/obp_api/resources/public_accounts/account.py">retrieve</a>(view_id, \*, bank_id, account_id) -> BinaryAPIResponse</code>

# UserInvitations

## SecretLink

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/user-invitations/SECRET_LINK">client.user_invitations.secret_link.<a href="./src/obp_api/resources/user_invitations/secret_link.py">retrieve</a>(bank_id) -> BinaryAPIResponse</code>

# UserCustomerLinks

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/user_customer_links">client.user_customer_links.<a href="./src/obp_api/resources/user_customer_links/user_customer_links.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/user_customer_link_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/banks/{BANK_ID}/user_customer_links/USER_CUSTOMER_LINK_ID">client.user_customer_links.<a href="./src/obp_api/resources/user_customer_links/user_customer_links.py">delete</a>(bank_id) -> None</code>

## Customers

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/user_customer_links/customers/{CUSTOMER_ID}">client.user_customer_links.customers.<a href="./src/obp_api/resources/user_customer_links/customers.py">list</a>(customer_id, \*, bank_id) -> BinaryAPIResponse</code>

## Users

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/user_customer_links/users/{USER_ID}">client.user_customer_links.users.<a href="./src/obp_api/resources/user_customer_links/users.py">list</a>(user_id, \*, bank_id) -> BinaryAPIResponse</code>

# Users

Methods:

- <code title="post /obp/v5.1.0/users">client.users.<a href="./src/obp_api/resources/users/users.py">create</a>(\*\*<a href="src/obp_api/types/user_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/users">client.users.<a href="./src/obp_api/resources/users/users.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/users/{USER_ID}">client.users.<a href="./src/obp_api/resources/users/users.py">delete</a>(user_id) -> None</code>
- <code title="post /obp/v5.1.0/management/user/reset-password-url">client.users.<a href="./src/obp_api/resources/users/users.py">reset_password_url</a>(\*\*<a href="src/obp_api/types/user_reset_password_url_params.py">params</a>) -> BinaryAPIResponse</code>

## Entitlements

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/users/{USER_ID}/entitlements">client.users.entitlements.<a href="./src/obp_api/resources/users/entitlements.py">list</a>(user_id, \*, bank_id) -> BinaryAPIResponse</code>

## AuthContextUpdates

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/users/current/auth-context-updates/{SCA_METHOD}">client.users.auth_context_updates.<a href="./src/obp_api/resources/users/auth_context_updates.py">create</a>(sca_method, \*, bank_id, \*\*<a href="src/obp_api/types/users/auth_context_update_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="post /obp/v5.1.0/banks/{BANK_ID}/users/current/auth-context-updates/{AUTH_CONTEXT_UPDATE_ID}/challenge">client.users.auth_context_updates.<a href="./src/obp_api/resources/users/auth_context_updates.py">challenge</a>(auth_context_update_id, \*, bank_id, \*\*<a href="src/obp_api/types/users/auth_context_update_challenge_params.py">params</a>) -> BinaryAPIResponse</code>

## Current

### Consumers

Methods:

- <code title="get /obp/v5.1.0/management/users/current/consumers">client.users.current.consumers.<a href="./src/obp_api/resources/users/current/consumers.py">list</a>() -> BinaryAPIResponse</code>

## Consents

Methods:

- <code title="get /obp/v5.1.0/user/current/consents/{CONSENT_ID}">client.users.consents.<a href="./src/obp_api/resources/users/consents.py">retrieve</a>(consent_id) -> BinaryAPIResponse</code>

## LockStatus

Methods:

- <code title="get /obp/v5.1.0/users/{PROVIDER}/{USERNAME}/lock-status">client.users.lock_status.<a href="./src/obp_api/resources/users/lock_status.py">retrieve</a>(username, \*, provider) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/users/{PROVIDER}/{USERNAME}/lock-status">client.users.lock_status.<a href="./src/obp_api/resources/users/lock_status.py">update</a>(username, \*, provider) -> BinaryAPIResponse</code>

## Locks

Methods:

- <code title="post /obp/v5.1.0/users/{PROVIDER}/{USERNAME}/locks">client.users.locks.<a href="./src/obp_api/resources/users/locks.py">create</a>(username, \*, provider) -> BinaryAPIResponse</code>

## AccountAccess

Methods:

- <code title="get /obp/v5.1.0/users/{USER_ID}/account-access">client.users.account_access.<a href="./src/obp_api/resources/users/account_access.py">list</a>(user_id) -> BinaryAPIResponse</code>

# Views

## Balances

Methods:

- <code title="get /obp/v5.1.0/banks/{BANK_ID}/views/{VIEW_ID}/balances">client.views.balances.<a href="./src/obp_api/resources/views/balances.py">list</a>(view_id, \*, bank_id) -> BinaryAPIResponse</code>

# WebHooks

## Notifications

Methods:

- <code title="post /obp/v5.1.0/banks/{BANK_ID}/web-hooks/account/notifications/on-create-transaction">client.web_hooks.notifications.<a href="./src/obp_api/resources/web_hooks/notifications.py">on_create_transaction</a>(bank_id, \*\*<a href="src/obp_api/types/web_hooks/notification_on_create_transaction_params.py">params</a>) -> BinaryAPIResponse</code>

# Cards

Methods:

- <code title="post /obp/v5.1.0/management/banks/{BANK_ID}/cards">client.cards.<a href="./src/obp_api/resources/cards/cards.py">create</a>(bank_id, \*\*<a href="src/obp_api/types/card_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/banks/{BANK_ID}/cards/{CARD_ID}">client.cards.<a href="./src/obp_api/resources/cards/cards.py">retrieve</a>(card_id, \*, bank_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/management/banks/{BANK_ID}/cards/{CARD_ID}">client.cards.<a href="./src/obp_api/resources/cards/cards.py">update</a>(card_id, \*, bank_id, \*\*<a href="src/obp_api/types/card_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/banks/{BANK_ID}/cards">client.cards.<a href="./src/obp_api/resources/cards/cards.py">list</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/management/banks/{BANK_ID}/cards/{CARD_ID}">client.cards.<a href="./src/obp_api/resources/cards/cards.py">delete</a>(card_id, \*, bank_id) -> None</code>

## Attribute

Methods:

- <code title="post /obp/v5.1.0/management/banks/{BANK_ID}/cards/{CARD_ID}/attribute">client.cards.attribute.<a href="./src/obp_api/resources/cards/attribute.py">create</a>(card_id, \*, bank_id, \*\*<a href="src/obp_api/types/cards/attribute_create_params.py">params</a>) -> BinaryAPIResponse</code>

## Attributes

Methods:

- <code title="put /obp/v5.1.0/management/banks/{BANK_ID}/cards/{CARD_ID}/attributes/{CARD_ATTRIBUTE_ID}">client.cards.attributes.<a href="./src/obp_api/resources/cards/attributes.py">update</a>(card_attribute_id, \*, bank_id, card_id, \*\*<a href="src/obp_api/types/cards/attribute_update_params.py">params</a>) -> BinaryAPIResponse</code>

# Certs

Methods:

- <code title="get /obp/v5.1.0/certs">client.certs.<a href="./src/obp_api/resources/certs.py">list</a>() -> BinaryAPIResponse</code>

# Config

Methods:

- <code title="get /obp/v5.1.0/config">client.config.<a href="./src/obp_api/resources/config.py">retrieve</a>() -> BinaryAPIResponse</code>

# Connector

Methods:

- <code title="get /obp/v5.1.0/connector/loopback">client.connector.<a href="./src/obp_api/resources/connector/connector.py">loopback</a>() -> BinaryAPIResponse</code>

## Metrics

Methods:

- <code title="get /obp/v5.1.0/management/connector/metrics">client.connector.metrics.<a href="./src/obp_api/resources/connector/metrics.py">list</a>() -> BinaryAPIResponse</code>

# Consumer

## ConsentRequests

Methods:

- <code title="post /obp/v5.1.0/consumer/consent-requests">client.consumer.consent_requests.<a href="./src/obp_api/resources/consumer/consent_requests/consent_requests.py">create</a>(\*\*<a href="src/obp_api/types/consumer/consent_request_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID">client.consumer.consent_requests.<a href="./src/obp_api/resources/consumer/consent_requests/consent_requests.py">retrieve</a>() -> BinaryAPIResponse</code>

### Email

#### Consents

Methods:

- <code title="post /obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID/EMAIL/consents">client.consumer.consent_requests.email.consents.<a href="./src/obp_api/resources/consumer/consent_requests/email/consents.py">create</a>() -> BinaryAPIResponse</code>

### Implicit

#### Consents

Methods:

- <code title="post /obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID/IMPLICIT/consents">client.consumer.consent_requests.implicit.consents.<a href="./src/obp_api/resources/consumer/consent_requests/implicit/consents.py">create</a>() -> BinaryAPIResponse</code>

### SMS

#### Consents

Methods:

- <code title="post /obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID/SMS/consents">client.consumer.consent_requests.sms.consents.<a href="./src/obp_api/resources/consumer/consent_requests/sms/consents.py">create</a>() -> BinaryAPIResponse</code>

### Consents

Methods:

- <code title="get /obp/v5.1.0/consumer/consent-requests/CONSENT_REQUEST_ID/consents">client.consumer.consent_requests.consents.<a href="./src/obp_api/resources/consumer/consent_requests/consents.py">retrieve</a>() -> BinaryAPIResponse</code>

# ConsentRequests

Methods:

- <code title="post /obp/v5.1.0/consumer/vrp-consent-requests">client.consent_requests.<a href="./src/obp_api/resources/consent_requests.py">create</a>(\*\*<a href="src/obp_api/types/consent_request_create_params.py">params</a>) -> BinaryAPIResponse</code>

# Consumers

Methods:

- <code title="post /obp/v5.1.0/management/consumers">client.consumers.<a href="./src/obp_api/resources/consumers/consumers.py">create</a>(\*\*<a href="src/obp_api/types/consumer_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/consumers/{CONSUMER_ID}">client.consumers.<a href="./src/obp_api/resources/consumers/consumers.py">retrieve</a>(consumer_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/management/consumers/{CONSUMER_ID}">client.consumers.<a href="./src/obp_api/resources/consumers/consumers.py">update</a>(consumer_id, \*\*<a href="src/obp_api/types/consumer_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/consumers">client.consumers.<a href="./src/obp_api/resources/consumers/consumers.py">list</a>() -> BinaryAPIResponse</code>

## Scopes

Methods:

- <code title="post /obp/v5.1.0/consumers/{CONSUMER_ID}/scopes">client.consumers.scopes.<a href="./src/obp_api/resources/consumers/scopes.py">create</a>(consumer_id, \*\*<a href="src/obp_api/types/consumers/scope_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/consumers/{CONSUMER_ID}/scopes">client.consumers.scopes.<a href="./src/obp_api/resources/consumers/scopes.py">list</a>(consumer_id) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/consumers/{CONSUMER_ID}/scope/{SCOPE_ID}">client.consumers.scopes.<a href="./src/obp_api/resources/consumers/scopes.py">delete</a>(scope_id, \*, consumer_id) -> None</code>

## CallLimits

Methods:

- <code title="get /obp/v5.1.0/management/consumers/{CONSUMER_ID}/consumer/call-limits">client.consumers.call_limits.<a href="./src/obp_api/resources/consumers/call_limits.py">retrieve</a>(consumer_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/management/consumers/{CONSUMER_ID}/consumer/call-limits">client.consumers.call_limits.<a href="./src/obp_api/resources/consumers/call_limits.py">update</a>(consumer_id, \*\*<a href="src/obp_api/types/consumers/call_limit_update_params.py">params</a>) -> BinaryAPIResponse</code>

## RedirectURL

Methods:

- <code title="put /obp/v5.1.0/management/consumers/{CONSUMER_ID}/consumer/redirect_url">client.consumers.redirect_url.<a href="./src/obp_api/resources/consumers/redirect_url.py">update</a>(consumer_id, \*\*<a href="src/obp_api/types/consumers/redirect_url_update_params.py">params</a>) -> BinaryAPIResponse</code>

# CustomersMinimal

Methods:

- <code title="get /obp/v5.1.0/customers-minimal">client.customers_minimal.<a href="./src/obp_api/resources/customers_minimal.py">list</a>() -> BinaryAPIResponse</code>

# Database

## Info

Methods:

- <code title="get /obp/v5.1.0/database/info">client.database.info.<a href="./src/obp_api/resources/database/info.py">retrieve</a>() -> BinaryAPIResponse</code>

# Development

## CallContext

Methods:

- <code title="get /obp/v5.1.0/development/call_context">client.development.call_context.<a href="./src/obp_api/resources/development/call_context.py">retrieve</a>() -> None</code>

## Echo

Methods:

- <code title="get /obp/v5.1.0/development/echo/jws-verified-request-jws-signed-response">client.development.echo.<a href="./src/obp_api/resources/development/echo.py">jws_verified_request_jws_signed_response</a>() -> None</code>

# DynamicRegistration

## Consumers

Methods:

- <code title="post /obp/v5.1.0/dynamic-registration/consumers">client.dynamic_registration.consumers.<a href="./src/obp_api/resources/dynamic_registration/consumers.py">create</a>(\*\*<a href="src/obp_api/types/dynamic_registration/consumer_create_params.py">params</a>) -> BinaryAPIResponse</code>

# Endpoints

## AuthenticationTypeValidations

Methods:

- <code title="get /obp/v5.1.0/endpoints/authentication-type-validations">client.endpoints.authentication_type_validations.<a href="./src/obp_api/resources/endpoints/authentication_type_validations.py">list</a>() -> BinaryAPIResponse</code>

## JsonSchemaValidations

Methods:

- <code title="get /obp/v5.1.0/endpoints/json-schema-validations">client.endpoints.json_schema_validations.<a href="./src/obp_api/resources/endpoints/json_schema_validations.py">list</a>() -> BinaryAPIResponse</code>

## Tags

Methods:

- <code title="post /obp/v5.1.0/management/endpoints/OPERATION_ID/tags">client.endpoints.tags.<a href="./src/obp_api/resources/endpoints/tags.py">create</a>(\*\*<a href="src/obp_api/types/endpoints/tag_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/management/endpoints/OPERATION_ID/tags/ENDPOINT_TAG_ID">client.endpoints.tags.<a href="./src/obp_api/resources/endpoints/tags.py">update</a>(\*\*<a href="src/obp_api/types/endpoints/tag_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/endpoints/OPERATION_ID/tags">client.endpoints.tags.<a href="./src/obp_api/resources/endpoints/tags.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/management/endpoints/OPERATION_ID/tags/ENDPOINT_TAG_ID">client.endpoints.tags.<a href="./src/obp_api/resources/endpoints/tags.py">delete</a>() -> BinaryAPIResponse</code>

# EntitlementRequests

Methods:

- <code title="post /obp/v5.1.0/entitlement-requests">client.entitlement_requests.<a href="./src/obp_api/resources/entitlement_requests.py">create</a>(\*\*<a href="src/obp_api/types/entitlement_request_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/my/entitlement-requests">client.entitlement_requests.<a href="./src/obp_api/resources/entitlement_requests.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/entitlement-requests/{ENTITLEMENT_REQUEST_ID}">client.entitlement_requests.<a href="./src/obp_api/resources/entitlement_requests.py">delete</a>(entitlement_request_id) -> None</code>

# Entitlements

Methods:

- <code title="get /obp/v5.1.0/my/entitlements">client.entitlements.<a href="./src/obp_api/resources/entitlements.py">list</a>() -> BinaryAPIResponse</code>

# JwksUris

Methods:

- <code title="get /obp/v5.1.0/jwks-uris">client.jwks_uris.<a href="./src/obp_api/resources/jwks_uris.py">retrieve</a>() -> BinaryAPIResponse</code>

# Management

## Accounts

Methods:

- <code title="post /obp/v5.1.0/management/accounts/account-routing-query">client.management.accounts.<a href="./src/obp_api/resources/management/accounts.py">account_routing_query</a>(\*\*<a href="src/obp_api/types/management/account_account_routing_query_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="post /obp/v5.1.0/management/accounts/account-routing-regex-query">client.management.accounts.<a href="./src/obp_api/resources/management/accounts.py">account_routing_regex_query</a>(\*\*<a href="src/obp_api/types/management/account_account_routing_regex_query_params.py">params</a>) -> BinaryAPIResponse</code>

## AggregateMetrics

Methods:

- <code title="get /obp/v5.1.0/management/aggregate-metrics">client.management.aggregate_metrics.<a href="./src/obp_api/resources/management/aggregate_metrics.py">list</a>() -> BinaryAPIResponse</code>

## APICollections

Methods:

- <code title="get /obp/v5.1.0/management/api-collections">client.management.api_collections.<a href="./src/obp_api/resources/management/api_collections.py">list</a>() -> BinaryAPIResponse</code>

## AuthenticationTypeValidations

Methods:

- <code title="get /obp/v5.1.0/management/authentication-type-validations/OPERATION_ID">client.management.authentication_type_validations.<a href="./src/obp_api/resources/management/authentication_type_validations.py">retrieve</a>() -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/management/authentication-type-validations/OPERATION_ID">client.management.authentication_type_validations.<a href="./src/obp_api/resources/management/authentication_type_validations.py">update</a>(\*\*<a href="src/obp_api/types/management/authentication_type_validation_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/authentication-type-validations">client.management.authentication_type_validations.<a href="./src/obp_api/resources/management/authentication_type_validations.py">list</a>() -> BinaryAPIResponse</code>

# AuthenticationTypeValidations

Methods:

- <code title="post /obp/v5.1.0/management/authentication-type-validations/OPERATION_ID">client.authentication_type_validations.<a href="./src/obp_api/resources/authentication_type_validations.py">create</a>(\*\*<a href="src/obp_api/types/authentication_type_validation_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/management/authentication-type-validations/OPERATION_ID">client.authentication_type_validations.<a href="./src/obp_api/resources/authentication_type_validations.py">delete</a>() -> BinaryAPIResponse</code>

# StandingOrders

Methods:

- <code title="post /obp/v5.1.0/management/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/standing-order">client.standing_orders.<a href="./src/obp_api/resources/standing_orders.py">create</a>(account_id, \*, bank_id, \*\*<a href="src/obp_api/types/standing_order_create_params.py">params</a>) -> BinaryAPIResponse</code>

# DynamicEndpoints

Methods:

- <code title="post /obp/v5.1.0/management/dynamic-endpoints">client.dynamic_endpoints.<a href="./src/obp_api/resources/dynamic_endpoints/dynamic_endpoints.py">create</a>(\*\*<a href="src/obp_api/types/dynamic_endpoint_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/dynamic-endpoints/DYNAMIC_ENDPOINT_ID">client.dynamic_endpoints.<a href="./src/obp_api/resources/dynamic_endpoints/dynamic_endpoints.py">retrieve</a>() -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/my/dynamic-endpoints">client.dynamic_endpoints.<a href="./src/obp_api/resources/dynamic_endpoints/dynamic_endpoints.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/my/dynamic-endpoints/DYNAMIC_ENDPOINT_ID">client.dynamic_endpoints.<a href="./src/obp_api/resources/dynamic_endpoints/dynamic_endpoints.py">delete</a>() -> None</code>

## Host

Methods:

- <code title="put /obp/v5.1.0/management/dynamic-endpoints/DYNAMIC_ENDPOINT_ID/host">client.dynamic_endpoints.host.<a href="./src/obp_api/resources/dynamic_endpoints/host.py">update</a>(\*\*<a href="src/obp_api/types/dynamic_endpoints/host_update_params.py">params</a>) -> BinaryAPIResponse</code>

# DynamicMessageDocs

Methods:

- <code title="post /obp/v5.1.0/management/dynamic-message-docs">client.dynamic_message_docs.<a href="./src/obp_api/resources/dynamic_message_docs.py">create</a>(\*\*<a href="src/obp_api/types/dynamic_message_doc_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/dynamic-message-docs/DYNAMIC_MESSAGE_DOC_ID">client.dynamic_message_docs.<a href="./src/obp_api/resources/dynamic_message_docs.py">retrieve</a>() -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/management/dynamic-message-docs/DYNAMIC_MESSAGE_DOC_ID">client.dynamic_message_docs.<a href="./src/obp_api/resources/dynamic_message_docs.py">update</a>(\*\*<a href="src/obp_api/types/dynamic_message_doc_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/dynamic-message-docs">client.dynamic_message_docs.<a href="./src/obp_api/resources/dynamic_message_docs.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/management/dynamic-message-docs/DYNAMIC_MESSAGE_DOC_ID">client.dynamic_message_docs.<a href="./src/obp_api/resources/dynamic_message_docs.py">delete</a>() -> BinaryAPIResponse</code>

# DynamicResourceDocs

Methods:

- <code title="post /obp/v5.1.0/management/dynamic-resource-docs">client.dynamic_resource_docs.<a href="./src/obp_api/resources/dynamic_resource_docs/dynamic_resource_docs.py">create</a>(\*\*<a href="src/obp_api/types/dynamic_resource_doc_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID">client.dynamic_resource_docs.<a href="./src/obp_api/resources/dynamic_resource_docs/dynamic_resource_docs.py">retrieve</a>() -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID">client.dynamic_resource_docs.<a href="./src/obp_api/resources/dynamic_resource_docs/dynamic_resource_docs.py">update</a>(\*\*<a href="src/obp_api/types/dynamic_resource_doc_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/dynamic-resource-docs">client.dynamic_resource_docs.<a href="./src/obp_api/resources/dynamic_resource_docs/dynamic_resource_docs.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/management/dynamic-resource-docs/DYNAMIC-RESOURCE-DOC-ID">client.dynamic_resource_docs.<a href="./src/obp_api/resources/dynamic_resource_docs/dynamic_resource_docs.py">delete</a>() -> BinaryAPIResponse</code>

## EndpointCode

Methods:

- <code title="post /obp/v5.1.0/management/dynamic-resource-docs/endpoint-code">client.dynamic_resource_docs.endpoint_code.<a href="./src/obp_api/resources/dynamic_resource_docs/endpoint_code.py">create</a>(\*\*<a href="src/obp_api/types/dynamic_resource_docs/endpoint_code_create_params.py">params</a>) -> BinaryAPIResponse</code>

# EndpointMappings

Methods:

- <code title="post /obp/v5.1.0/management/endpoint-mappings">client.endpoint_mappings.<a href="./src/obp_api/resources/endpoint_mappings.py">create</a>(\*\*<a href="src/obp_api/types/endpoint_mapping_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID">client.endpoint_mappings.<a href="./src/obp_api/resources/endpoint_mappings.py">retrieve</a>() -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID">client.endpoint_mappings.<a href="./src/obp_api/resources/endpoint_mappings.py">update</a>(\*\*<a href="src/obp_api/types/endpoint_mapping_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/endpoint-mappings">client.endpoint_mappings.<a href="./src/obp_api/resources/endpoint_mappings.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/management/endpoint-mappings/ENDPOINT_MAPPING_ID">client.endpoint_mappings.<a href="./src/obp_api/resources/endpoint_mappings.py">delete</a>() -> BinaryAPIResponse</code>

# FastFirehoseAccounts

Methods:

- <code title="get /obp/v5.1.0/management/banks/{BANK_ID}/fast-firehose/accounts">client.fast_firehose_accounts.<a href="./src/obp_api/resources/fast_firehose_accounts.py">list</a>(bank_id) -> BinaryAPIResponse</code>

# CascadingBanks

Methods:

- <code title="delete /obp/v5.1.0/management/cascading/banks/{BANK_ID}">client.cascading_banks.<a href="./src/obp_api/resources/cascading_banks/cascading_banks.py">delete</a>(bank_id) -> None</code>

## Accounts

Methods:

- <code title="delete /obp/v5.1.0/management/cascading/banks/{BANK_ID}/accounts/{ACCOUNT_ID}">client.cascading_banks.accounts.<a href="./src/obp_api/resources/cascading_banks/accounts/accounts.py">delete</a>(account_id, \*, bank_id) -> None</code>

### Transactions

Methods:

- <code title="delete /obp/v5.1.0/management/cascading/banks/{BANK_ID}/accounts/{ACCOUNT_ID}/transactions/{TRANSACTION_ID}">client.cascading_banks.accounts.transactions.<a href="./src/obp_api/resources/cascading_banks/accounts/transactions.py">delete</a>(transaction_id, \*, bank_id, account_id) -> None</code>

# ConnectorMethods

Methods:

- <code title="post /obp/v5.1.0/management/connector-methods">client.connector_methods.<a href="./src/obp_api/resources/connector_methods.py">create</a>(\*\*<a href="src/obp_api/types/connector_method_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/connector-methods/CONNECTOR_METHOD_ID">client.connector_methods.<a href="./src/obp_api/resources/connector_methods.py">retrieve</a>() -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/management/connector-methods/CONNECTOR_METHOD_ID">client.connector_methods.<a href="./src/obp_api/resources/connector_methods.py">update</a>(\*\*<a href="src/obp_api/types/connector_method_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/connector-methods">client.connector_methods.<a href="./src/obp_api/resources/connector_methods.py">list</a>() -> BinaryAPIResponse</code>

# JsonSchemaValidations

Methods:

- <code title="post /obp/v5.1.0/management/json-schema-validations/OPERATION_ID">client.json_schema_validations.<a href="./src/obp_api/resources/json_schema_validations.py">create</a>(\*\*<a href="src/obp_api/types/json_schema_validation_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/json-schema-validations/OPERATION_ID">client.json_schema_validations.<a href="./src/obp_api/resources/json_schema_validations.py">retrieve</a>() -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/management/json-schema-validations/OPERATION_ID">client.json_schema_validations.<a href="./src/obp_api/resources/json_schema_validations.py">update</a>(\*\*<a href="src/obp_api/types/json_schema_validation_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/json-schema-validations">client.json_schema_validations.<a href="./src/obp_api/resources/json_schema_validations.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/management/json-schema-validations/OPERATION_ID">client.json_schema_validations.<a href="./src/obp_api/resources/json_schema_validations.py">delete</a>() -> BinaryAPIResponse</code>

# MethodRoutings

Methods:

- <code title="post /obp/v5.1.0/management/method_routings">client.method_routings.<a href="./src/obp_api/resources/method_routings.py">create</a>(\*\*<a href="src/obp_api/types/method_routing_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/management/method_routings/{METHOD_ROUTING_ID}">client.method_routings.<a href="./src/obp_api/resources/method_routings.py">update</a>(method_routing_id, \*\*<a href="src/obp_api/types/method_routing_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/method_routings">client.method_routings.<a href="./src/obp_api/resources/method_routings.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/management/method_routings/{METHOD_ROUTING_ID}">client.method_routings.<a href="./src/obp_api/resources/method_routings.py">delete</a>(method_routing_id) -> None</code>

# Metrics

Methods:

- <code title="get /obp/v5.1.0/management/metrics">client.metrics.<a href="./src/obp_api/resources/metrics/metrics.py">list</a>() -> BinaryAPIResponse</code>

## Banks

Methods:

- <code title="get /obp/v5.1.0/management/metrics/banks/{BANK_ID}">client.metrics.banks.<a href="./src/obp_api/resources/metrics/banks.py">retrieve</a>(bank_id) -> BinaryAPIResponse</code>

## TopAPIs

Methods:

- <code title="get /obp/v5.1.0/management/metrics/top-apis">client.metrics.top_apis.<a href="./src/obp_api/resources/metrics/top_apis.py">list</a>() -> BinaryAPIResponse</code>

## TopConsumers

Methods:

- <code title="get /obp/v5.1.0/management/metrics/top-consumers">client.metrics.top_consumers.<a href="./src/obp_api/resources/metrics/top_consumers.py">list</a>() -> BinaryAPIResponse</code>

# SystemDynamicEntities

Methods:

- <code title="post /obp/v5.1.0/management/system-dynamic-entities">client.system_dynamic_entities.<a href="./src/obp_api/resources/system_dynamic_entities.py">create</a>(\*\*<a href="src/obp_api/types/system_dynamic_entity_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/management/system-dynamic-entities/{DYNAMIC_ENTITY_ID}">client.system_dynamic_entities.<a href="./src/obp_api/resources/system_dynamic_entities.py">update</a>(dynamic_entity_id, \*\*<a href="src/obp_api/types/system_dynamic_entity_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/system-dynamic-entities">client.system_dynamic_entities.<a href="./src/obp_api/resources/system_dynamic_entities.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/management/system-dynamic-entities/{DYNAMIC_ENTITY_ID}">client.system_dynamic_entities.<a href="./src/obp_api/resources/system_dynamic_entities.py">delete</a>(dynamic_entity_id) -> None</code>

# SystemIntegrity

Methods:

- <code title="get /obp/v5.1.0/management/system/integrity/account-access-unique-index-1-check">client.system_integrity.<a href="./src/obp_api/resources/system_integrity/system_integrity.py">account_access_unique_index_1_check</a>() -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/system/integrity/custom-view-names-check">client.system_integrity.<a href="./src/obp_api/resources/system_integrity/system_integrity.py">custom_view_names_check</a>() -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/system/integrity/system-view-names-check">client.system_integrity.<a href="./src/obp_api/resources/system_integrity/system_integrity.py">system_view_names_check</a>() -> BinaryAPIResponse</code>

## Banks

Methods:

- <code title="get /obp/v5.1.0/management/system/integrity/banks/{BANK_ID}/account-currency-check">client.system_integrity.banks.<a href="./src/obp_api/resources/system_integrity/banks.py">account_currency_check</a>(bank_id) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/system/integrity/banks/{BANK_ID}/orphaned-account-check">client.system_integrity.banks.<a href="./src/obp_api/resources/system_integrity/banks.py">orphaned_account_check</a>(bank_id) -> BinaryAPIResponse</code>

# WebuiProps

Methods:

- <code title="post /obp/v5.1.0/management/webui_props">client.webui_props.<a href="./src/obp_api/resources/webui_props.py">create</a>(\*\*<a href="src/obp_api/types/webui_prop_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/management/webui_props">client.webui_props.<a href="./src/obp_api/resources/webui_props.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/management/webui_props/{WEB_UI_PROPS_ID}">client.webui_props.<a href="./src/obp_api/resources/webui_props.py">delete</a>(web_ui_props_id) -> None</code>

# Documentation

## MessageDocs

Methods:

- <code title="get /obp/v5.1.0/message-docs/CONNECTOR">client.documentation.message_docs.<a href="./src/obp_api/resources/documentation/message_docs/message_docs.py">retrieve</a>() -> BinaryAPIResponse</code>

### Swagger2

Methods:

- <code title="get /obp/v5.1.0/message-docs/CONNECTOR/swagger2.0">client.documentation.message_docs.swagger2.<a href="./src/obp_api/resources/documentation/message_docs/swagger2.py">\_0</a>() -> BinaryAPIResponse</code>

# Consent

Methods:

- <code title="delete /obp/v5.1.0/my/consent/current">client.consent.<a href="./src/obp_api/resources/consent.py">revoke</a>() -> BinaryAPIResponse</code>

# CorrelatedEntities

Methods:

- <code title="get /obp/v5.1.0/my/correlated-entities">client.correlated_entities.<a href="./src/obp_api/resources/correlated_entities.py">list</a>() -> BinaryAPIResponse</code>

# DynamicEntities

Methods:

- <code title="put /obp/v5.1.0/my/dynamic-entities/{DYNAMIC_ENTITY_ID}">client.dynamic_entities.<a href="./src/obp_api/resources/dynamic_entities.py">update</a>(dynamic_entity_id, \*\*<a href="src/obp_api/types/dynamic_entity_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/my/dynamic-entities">client.dynamic_entities.<a href="./src/obp_api/resources/dynamic_entities.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/my/dynamic-entities/{DYNAMIC_ENTITY_ID}">client.dynamic_entities.<a href="./src/obp_api/resources/dynamic_entities.py">delete</a>(dynamic_entity_id) -> None</code>

# Mtls

## Certificate

### Current

Methods:

- <code title="get /obp/v5.1.0/my/mtls/certificate/current">client.mtls.certificate.current.<a href="./src/obp_api/resources/mtls/certificate/current.py">retrieve</a>() -> BinaryAPIResponse</code>

# Spaces

Methods:

- <code title="get /obp/v5.1.0/my/spaces">client.spaces.<a href="./src/obp_api/resources/spaces.py">list</a>() -> BinaryAPIResponse</code>

# User

## Attributes

Methods:

- <code title="post /obp/v5.1.0/my/user/attributes">client.user.attributes.<a href="./src/obp_api/resources/user/attributes.py">create</a>(\*\*<a href="src/obp_api/types/user/attribute_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/my/user/attributes/USER_ATTRIBUTE_ID">client.user.attributes.<a href="./src/obp_api/resources/user/attributes.py">update</a>(\*\*<a href="src/obp_api/types/user/attribute_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/my/user/attributes">client.user.attributes.<a href="./src/obp_api/resources/user/attributes.py">list</a>() -> BinaryAPIResponse</code>

# RateLimits

Methods:

- <code title="get /obp/v5.1.0/rate-limiting">client.rate_limits.<a href="./src/obp_api/resources/rate_limits.py">retrieve</a>() -> BinaryAPIResponse</code>

# RegulatedEntities

Methods:

- <code title="post /obp/v5.1.0/regulated-entities">client.regulated_entities.<a href="./src/obp_api/resources/regulated_entities.py">create</a>(\*\*<a href="src/obp_api/types/regulated_entity_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/regulated-entities/REGULATED_ENTITY_ID">client.regulated_entities.<a href="./src/obp_api/resources/regulated_entities.py">retrieve</a>() -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/regulated-entities">client.regulated_entities.<a href="./src/obp_api/resources/regulated_entities.py">list</a>() -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/regulated-entities/REGULATED_ENTITY_ID">client.regulated_entities.<a href="./src/obp_api/resources/regulated_entities.py">delete</a>() -> None</code>

# ResourceDocs

Methods:

- <code title="get /obp/v5.1.0/resource-docs/{API_VERSION}/obp">client.resource_docs.<a href="./src/obp_api/resources/resource_docs.py">list</a>(api_version) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/resource-docs/{API_VERSION}/swagger">client.resource_docs.<a href="./src/obp_api/resources/resource_docs.py">swagger</a>(api_version) -> BinaryAPIResponse</code>

# Roles

Methods:

- <code title="get /obp/v5.1.0/roles">client.roles.<a href="./src/obp_api/resources/roles.py">list</a>() -> BinaryAPIResponse</code>

# Sandbox

Methods:

- <code title="post /obp/v5.1.0/sandbox/data-import">client.sandbox.<a href="./src/obp_api/resources/sandbox.py">data_import</a>(\*\*<a href="src/obp_api/types/sandbox_data_import_params.py">params</a>) -> BinaryAPIResponse</code>

# Search

## Metrics

Methods:

- <code title="get /obp/v5.1.0/search/metrics">client.search.metrics.<a href="./src/obp_api/resources/search/metrics.py">list</a>() -> BinaryAPIResponse</code>

## Warehouse

Methods:

- <code title="post /obp/v5.1.0/search/warehouse/{INDEX}">client.search.warehouse.<a href="./src/obp_api/resources/search/warehouse/warehouse.py">create</a>(index, \*\*<a href="src/obp_api/types/search/warehouse_create_params.py">params</a>) -> BinaryAPIResponse</code>

### Statistics

Methods:

- <code title="post /obp/v5.1.0/search/warehouse/statistics/{INDEX}/{FIELD}">client.search.warehouse.statistics.<a href="./src/obp_api/resources/search/warehouse/statistics.py">create</a>(field, \*, index, \*\*<a href="src/obp_api/types/search/warehouse/statistic_create_params.py">params</a>) -> BinaryAPIResponse</code>

# SystemViews

Methods:

- <code title="post /obp/v5.1.0/system-views">client.system_views.<a href="./src/obp_api/resources/system_views/system_views.py">create</a>(\*\*<a href="src/obp_api/types/system_view_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /obp/v5.1.0/system-views/{VIEW_ID}">client.system_views.<a href="./src/obp_api/resources/system_views/system_views.py">retrieve</a>(view_id) -> BinaryAPIResponse</code>
- <code title="put /obp/v5.1.0/system-views/{VIEW_ID}">client.system_views.<a href="./src/obp_api/resources/system_views/system_views.py">update</a>(view_id, \*\*<a href="src/obp_api/types/system_view_update_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="delete /obp/v5.1.0/system-views/{VIEW_ID}">client.system_views.<a href="./src/obp_api/resources/system_views/system_views.py">delete</a>(view_id) -> None</code>

## IDs

Methods:

- <code title="get /obp/v5.1.0/system-views-ids">client.system_views.ids.<a href="./src/obp_api/resources/system_views/ids.py">list</a>() -> BinaryAPIResponse</code>

# UserEntitlements

Methods:

- <code title="post /obp/v5.1.0/user-entitlements">client.user_entitlements.<a href="./src/obp_api/resources/user_entitlements.py">create</a>(\*\*<a href="src/obp_api/types/user_entitlement_create_params.py">params</a>) -> BinaryAPIResponse</code>
