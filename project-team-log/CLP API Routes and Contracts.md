## Supported endpoints:
Note: All API calls require TOKEN: <token_value> header. All communications are performed with the application/json content type.
1. /application - to use the endpoint, the application must have `MasterApp` access level.
   1. POST request - create a new application: CreateApplicationRequest -> ApplicationDataResponse
      1. Request body:
         * application_name - str (30 chars)
         * access_level - Enum[`Can_Read`, `Can_Modify_Orders`]
      2. General Response body (ResponseStatus):
         * success - bool
      3. Successful Response body (ApplicationDataResponse):
         * app_id - str
         * Token - str
      4. Returned errors:
         * 401 Unauthorized - if no token provided
         * 403 Forbidden - if the app does not have a sufficient access level
   2. PUT request - modify existing application: UpdateApplicationRequest -> ResponseStatus
      1. Request body:
         * app_id - str
         * new_access_level - Enum[`Can_Read`, `Can_Modify_Orders`]
      2. General Response body (ResponseStatus):
         * success - bool
      3. Successful Response body (ApplicationDataResponse):
         * app_id - str
         * Token - str
      4. Returned errors:
         * 401 Unauthorized - if no token provided
         * 403 Forbidden - if the app does not have a sufficient access level
   3. DELETE Request - delete existing application: DeleteApplicationRequest -> ResponseStatus
      1. Request body:
         * app_id - str
      2. Response body (ResponseStatus):
         * success: bool
      3. Returned errors:
         * 401 Unauthorized - if no token provided
         * 403 Forbidden - if the app does not have a sufficient access level
2. /user - to use the endpoint, the application must have `Can_Read` access level.
   1. GET request - retrieve current user's balance
      1. Request Parameters (UserBalanceRequest):
         * user_id - int (passed as a query parameter in the URL, e.g., /user?user_id=123)
      2. General Response body (ResponseStatus):
         * success - bool
      3. Successful Response body (UserBalanceResponse):
         * current_balance - int
      4. Returned errors:
         * 401 Unauthorized - if no token provided
         * 403 Forbidden - if the app does not have a sufficient access level
         * 404 Not Found - if the user does not exist
3. /orders - to use the endpoint, the application must have `Can_Modify_Orders` access level.
   1. POST request - insert an order to the system to calculate the loyalty points increase: 
   CreateOrderRequest -> ResponseStatus
      1. Request Body:
         * user_id - int
         * order_id - int
         * total_cost - int
         * completed_at - int
      2. Response body (ResponseStatus):
         * success - bool
      3. Returned errors:
         * 401 Unauthorized - if no token provided
         * 403 Forbidden - if the app does not have a sufficient access level
   3. DELETE request - delete an order (in case if the order was returned): DeleteOrderRequest -> ResponseStatus
      1. Request Body:
         * order_id - int
      2. Response body (ResponseStatus):
         * success - bool
      3. Returned errors:
         * 401 Unauthorized - if no token provided
         * 403 Forbidden - if the app does not have a sufficient access level
## Contracts:
0. Utility Contracts:
   1. AccessLevel - Enum[`Can_Read`, `Can_Modify_Orders`]
1. Request Contracts:
   1. CreateApplicationRequest:
      * application_name - str (30 chars)
      * access_level - AccessLevel (0.i contract)
   2. UpdateApplicationRequest:
      * app_id - str
      * new_access_level - AccessLevel (0.i contract)
   3. DeleteApplicationRequest:
      * app_id - str
   4. UserBalanceRequest:
      * user_id - int
   5. CreateOrderRequest:
      * user_id - int
      * order_id - int
      * total_cost - int
      * completed_at - int
   6. DeleteOrderRequest:
      * order_id - int
2. Response Contracts:
   1. ResponseStatus:
      * success - bool
   2. ApplicationDataResponse(ResponseStatus):
      * app_id - str
      * token - str
   3. UserBalanceResponse(ResponseStatus):
      * current_balance - int
