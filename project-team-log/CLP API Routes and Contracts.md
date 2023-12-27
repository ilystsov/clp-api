## Supported endpoints:
Note: All API calls require TOKEN: <token_value> header. All communications are performed with the application/json content type.
1. /application - to use the endpoint, the application must have `MasterApp` access level.
   1. POST request - create a new application: CreateApplicationRequest -> CreateApplicationResponse
      1. Request body:
         * ApplicationName - str (30 chars)
         * AccessLevel - Enum[`Can_Read`, `Can_Modify_Orders`]
      2. General Response body (ResponseStatus):
         * success - bool
      3. Successful Response body (CreateApplicationResponse):
         * AppID - str
         * Token - str
      4. Returned errors:
         * 401 Unauthorized - if no token provided
         * 403 Forbidden - if the app does not have a sufficient access level
   2. PUT request - modify existing application: UpdateApplicationRequest -> ResponseStatus
      1. Request body:
         * AppID - str
         * NewAccessLevel - Enum[`Can_Read`, `Can_Modify_Orders`]
      2. Response body (ResponseStatus):
         * success: bool
      3. Returned errors:
         * 401 Unauthorized - if no token provided
         * 403 Forbidden - if the app does not have a sufficient access level
   3. DELETE Request - delete existing application: DeleteApplicationRequest -> ResponseStatus
      1. Request body:
         * AppID - str
      2. Response body (ResponseStatus):
         * success: bool
      3. Returned errors:
         * 401 Unauthorized - if no token provided
         * 403 Forbidden - if the app does not have a sufficient access level
2. /user - to use the endpoint, the application must have `Can_Read` access level.
   1. GET request - retrieve current user's balance
      1. Request Parameters (UserBalanceRequest):
         * UserID - int (passed as a query parameter in the URL, e.g., /user?UserID=123)
      2. General Response body (ResponseStatus):
         * success - bool
      3. Successful Response body (UserBalanceResponse):
         * CurrentBalance - int
      4. Returned errors:
         * 401 Unauthorized - if no token provided
         * 403 Forbidden - if the app does not have a sufficient access level
         * 404 Not Found - if the user does not exist
3. /orders - to use the endpoint, the application must have `Can_Modify_Orders` access level.
   1. POST request - insert an order to the system to calculate the loyalty points increase: 
   CreateOrderRequest -> ResponseStatus
      1. Request Body:
         * UserID - int
         * OrderID - int
         * TotalCost - int
         * CompletedAt - int
      2. Response body (ResponseStatus):
         * success - bool
      3. Returned errors:
         * 401 Unauthorized - if no token provided
         * 403 Forbidden - if the app does not have a sufficient access level
   3. DELETE request - delete an order (in case if the order was returned): DeleteOrderRequest -> ResponseStatus
      1. Request Body:
         * OrderID - int
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
      * ApplicationName - str (30 chars)
      * AccessLevel - AccessLevel (0.i contract)
   2. UpdateApplicationRequest:
      * AppID - str
      * NewAccessLevel - AccessLevel (0.i contract)
   3. DeleteApplicationRequest:
      * AppID - str
   4. UserBalanceRequest:
      * UserID - int
   5. CreateOrderRequest:
      * UserID - int
      * OrderID - int
      * TotalCost - int
      * CompletedAt - int
   6. DeleteOrderRequest:
      * OrderID - int
2. Response Contracts:
   1. ResponseStatus:
      * success - bool
   2. CreateApplicationResponse(ResponseStatus):
      * AppID - str
      * Token - str
   3. UserBalanceResponse(ResponseStatus):
      * CurrentBalance - int
