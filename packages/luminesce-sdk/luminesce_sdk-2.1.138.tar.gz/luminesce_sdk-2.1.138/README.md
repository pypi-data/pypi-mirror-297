<a id="documentation-for-api-endpoints"></a>
## Documentation for API Endpoints

All URIs are relative to *https://fbn-prd.lusid.com/honeycomb*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*ApplicationMetadataApi* | [**get_services_as_access_controlled_resources**](docs/ApplicationMetadataApi.md#get_services_as_access_controlled_resources) | **GET** /api/metadata/access/resources | GetServicesAsAccessControlledResources: Get resources available for access control
*BinaryDownloadingApi* | [**download_binary**](docs/BinaryDownloadingApi.md#download_binary) | **GET** /api/Download/download | [EXPERIMENTAL] DownloadBinary: Downloads the latest version (or specific if needs be) of the specified Luminesce Binary, given the required entitlements.
*BinaryDownloadingApi* | [**get_binary_versions**](docs/BinaryDownloadingApi.md#get_binary_versions) | **GET** /api/Download/versions | [EXPERIMENTAL] GetBinaryVersions: Gets the list of available versions of a user-downloadable binary from Nexus
*CertificateManagementApi* | [**download_certificate**](docs/CertificateManagementApi.md#download_certificate) | **GET** /api/Certificate/certificate | [EXPERIMENTAL] DownloadCertificate: Downloads your latest Domain or User certificate's public or private key - if any
*CertificateManagementApi* | [**list_certificates**](docs/CertificateManagementApi.md#list_certificates) | **GET** /api/Certificate/certificates | [EXPERIMENTAL] ListCertificates: Lists all the certificates previously minted to which you have access
*CertificateManagementApi* | [**manage_certificate**](docs/CertificateManagementApi.md#manage_certificate) | **PUT** /api/Certificate/manage | [EXPERIMENTAL] ManageCertificate: Manages a new certificate (Create / Renew / Revoke)
*CurrentTableFieldCatalogApi* | [**get_catalog**](docs/CurrentTableFieldCatalogApi.md#get_catalog) | **GET** /api/Catalog | GetCatalog: Shows Table and Field level information on Providers that are currently running that you have access to (in Json format)
*CurrentTableFieldCatalogApi* | [**get_fields**](docs/CurrentTableFieldCatalogApi.md#get_fields) | **GET** /api/Catalog/fields | GetFields: Shows Table level information on Providers that are currently running that you have access to (in Json format)
*CurrentTableFieldCatalogApi* | [**get_providers**](docs/CurrentTableFieldCatalogApi.md#get_providers) | **GET** /api/Catalog/providers | GetProviders: Shows Table level information on Providers that are currently running that you have access to (in Json format)
*HealthCheckingEndpointApi* | [**fake_node_reclaim**](docs/HealthCheckingEndpointApi.md#fake_node_reclaim) | **GET** /fakeNodeReclaim | [INTERNAL] FakeNodeReclaim: An internal Method used to mark the next SIGTERM as though an Aws Node reclaim were about to take place.
*HistoricallyExecutedQueriesApi* | [**cancel_history**](docs/HistoricallyExecutedQueriesApi.md#cancel_history) | **DELETE** /api/History/{executionId} | CancelHistory: Cancels (if running) or clears the data from (if completed) a previously started History query
*HistoricallyExecutedQueriesApi* | [**fetch_history_result_histogram**](docs/HistoricallyExecutedQueriesApi.md#fetch_history_result_histogram) | **GET** /api/History/{executionId}/histogram | FetchHistoryResultHistogram: Fetches the result from a previously started query, converts it to a histogram (counts in buckets).
*HistoricallyExecutedQueriesApi* | [**fetch_history_result_json**](docs/HistoricallyExecutedQueriesApi.md#fetch_history_result_json) | **GET** /api/History/{executionId}/json | FetchHistoryResultJson: Fetches the result from a previously started query, in JSON format.
*HistoricallyExecutedQueriesApi* | [**get_history**](docs/HistoricallyExecutedQueriesApi.md#get_history) | **GET** /api/History | GetHistory: Shows queries executed in a given historical time window (in Json format).
*HistoricallyExecutedQueriesApi* | [**get_progress_of_history**](docs/HistoricallyExecutedQueriesApi.md#get_progress_of_history) | **GET** /api/History/{executionId} | GetProgressOfHistory: View progress information (up until this point) of a history query
*MultiQueryExecutionApi* | [**cancel_multi_query**](docs/MultiQueryExecutionApi.md#cancel_multi_query) | **DELETE** /api/MultiQueryBackground/{executionId} | CancelMultiQuery: Cancels (if running) or clears the data from (if completed) a previously started query-set
*MultiQueryExecutionApi* | [**get_progress_of_multi_query**](docs/MultiQueryExecutionApi.md#get_progress_of_multi_query) | **GET** /api/MultiQueryBackground/{executionId} | GetProgressOfMultiQuery: View progress information (up until this point) for the entire query-set
*MultiQueryExecutionApi* | [**start_queries**](docs/MultiQueryExecutionApi.md#start_queries) | **PUT** /api/MultiQueryBackground | StartQueries: Starts to Execute the LuminesceSql statements in the background.
*SqlBackgroundExecutionApi* | [**cancel_query**](docs/SqlBackgroundExecutionApi.md#cancel_query) | **DELETE** /api/SqlBackground/{executionId} | CancelQuery: Cancels (if running) or clears the data from (if completed) a previously started query
*SqlBackgroundExecutionApi* | [**fetch_query_result_csv**](docs/SqlBackgroundExecutionApi.md#fetch_query_result_csv) | **GET** /api/SqlBackground/{executionId}/csv | FetchQueryResultCsv: Fetches the result from a previously started query, in CSV format.
*SqlBackgroundExecutionApi* | [**fetch_query_result_excel**](docs/SqlBackgroundExecutionApi.md#fetch_query_result_excel) | **GET** /api/SqlBackground/{executionId}/excel | FetchQueryResultExcel: Fetches the result from a previously started query, in Excel format.
*SqlBackgroundExecutionApi* | [**fetch_query_result_histogram**](docs/SqlBackgroundExecutionApi.md#fetch_query_result_histogram) | **GET** /api/SqlBackground/{executionId}/histogram | FetchQueryResultHistogram: Fetches the result from a previously started query, converts it to a histogram (counts in buckets).
*SqlBackgroundExecutionApi* | [**fetch_query_result_json**](docs/SqlBackgroundExecutionApi.md#fetch_query_result_json) | **GET** /api/SqlBackground/{executionId}/json | FetchQueryResultJson: Fetches the result from a previously started query, in JSON string format.  Please move to '/jsonProper' instead.  This may be marked as Deprecated in the future.
*SqlBackgroundExecutionApi* | [**fetch_query_result_json_proper**](docs/SqlBackgroundExecutionApi.md#fetch_query_result_json_proper) | **GET** /api/SqlBackground/{executionId}/jsonProper | FetchQueryResultJsonProper: Fetches the result from a previously started query, in JSON format.
*SqlBackgroundExecutionApi* | [**fetch_query_result_parquet**](docs/SqlBackgroundExecutionApi.md#fetch_query_result_parquet) | **GET** /api/SqlBackground/{executionId}/parquet | FetchQueryResultParquet: Fetches the result from a previously started query, in Parquet format.
*SqlBackgroundExecutionApi* | [**fetch_query_result_pipe**](docs/SqlBackgroundExecutionApi.md#fetch_query_result_pipe) | **GET** /api/SqlBackground/{executionId}/pipe | FetchQueryResultPipe: Fetches the result from a previously started query, in pipe-delimited format.
*SqlBackgroundExecutionApi* | [**fetch_query_result_sqlite**](docs/SqlBackgroundExecutionApi.md#fetch_query_result_sqlite) | **GET** /api/SqlBackground/{executionId}/sqlite | FetchQueryResultSqlite: Fetches the result from a previously started query, in SqLite format.
*SqlBackgroundExecutionApi* | [**fetch_query_result_xml**](docs/SqlBackgroundExecutionApi.md#fetch_query_result_xml) | **GET** /api/SqlBackground/{executionId}/xml | FetchQueryResultXml: Fetches the result from a previously started query, in Xml format.
*SqlBackgroundExecutionApi* | [**get_progress_of**](docs/SqlBackgroundExecutionApi.md#get_progress_of) | **GET** /api/SqlBackground/{executionId} | GetProgressOf: View progress information (up until this point)
*SqlBackgroundExecutionApi* | [**start_query**](docs/SqlBackgroundExecutionApi.md#start_query) | **PUT** /api/SqlBackground | StartQuery: Starts to Execute LuminesceSql in the background.
*SqlDesignApi* | [**put_case_statement_design_sql_to_design**](docs/SqlDesignApi.md#put_case_statement_design_sql_to_design) | **PUT** /api/Sql/tocasestatementdesign | [EXPERIMENTAL] PutCaseStatementDesignSqlToDesign: Converts SQL queries to a CaseStatementDesign object.
*SqlDesignApi* | [**put_case_statement_design_to_sql**](docs/SqlDesignApi.md#put_case_statement_design_to_sql) | **PUT** /api/Sql/fromcasestatementdesign | [EXPERIMENTAL] PutCaseStatementDesignToSql: Generates SQL case statement queries from a structured design
*SqlDesignApi* | [**put_file_read_design_to_sql**](docs/SqlDesignApi.md#put_file_read_design_to_sql) | **PUT** /api/Sql/fromfilereaddesign | [EXPERIMENTAL] PutFileReadDesignToSql: Generates file read SQL from a structured query design
*SqlDesignApi* | [**put_inlined_properties_design_sql_to_design**](docs/SqlDesignApi.md#put_inlined_properties_design_sql_to_design) | **PUT** /api/Sql/toinlinedpropertiesdesign | [EXPERIMENTAL] PutInlinedPropertiesDesignSqlToDesign: Generates a SQL-inlined-properties-design object from SQL string, if possible.
*SqlDesignApi* | [**put_inlined_properties_design_to_sql**](docs/SqlDesignApi.md#put_inlined_properties_design_to_sql) | **PUT** /api/Sql/frominlinedpropertiesdesign | [EXPERIMENTAL] PutInlinedPropertiesDesignToSql: Generates inlined properties SQL from a structured design
*SqlDesignApi* | [**put_intellisense**](docs/SqlDesignApi.md#put_intellisense) | **PUT** /api/Sql/intellisense | PutIntellisense: Generate a set of possible intellisense prompts given a SQL snip-it (in need not yet be valid) and cursor location
*SqlDesignApi* | [**put_intellisense_error**](docs/SqlDesignApi.md#put_intellisense_error) | **PUT** /api/Sql/intellisenseError | PutIntellisenseError: Generate a set of error ranges, if any, in the given SQL (expressed as Lines)
*SqlDesignApi* | [**put_query_design_to_sql**](docs/SqlDesignApi.md#put_query_design_to_sql) | **PUT** /api/Sql/fromdesign | [EXPERIMENTAL] PutQueryDesignToSql: Generates SQL from a structured query design
*SqlDesignApi* | [**put_query_to_format**](docs/SqlDesignApi.md#put_query_to_format) | **PUT** /api/Sql/pretty | PutQueryToFormat: Formats SQL into a more readable form, a.k.a. Pretty-Print the SQL.
*SqlDesignApi* | [**put_sql_to_extract_scalar_parameters**](docs/SqlDesignApi.md#put_sql_to_extract_scalar_parameters) | **PUT** /api/Sql/extractscalarparameters | [EXPERIMENTAL] PutSqlToExtractScalarParameters: Generates information about all the scalar parameters defined in the given SQL statement
*SqlDesignApi* | [**put_sql_to_file_read_design**](docs/SqlDesignApi.md#put_sql_to_file_read_design) | **PUT** /api/Sql/tofilereaddesign | [EXPERIMENTAL] PutSqlToFileReadDesign: Generates a SQL-file-read-design object from SQL string, if possible.
*SqlDesignApi* | [**put_sql_to_query_design**](docs/SqlDesignApi.md#put_sql_to_query_design) | **PUT** /api/Sql/todesign | [EXPERIMENTAL] PutSqlToQueryDesign: Generates a SQL-design object from SQL string, if possible.
*SqlDesignApi* | [**put_sql_to_view_design**](docs/SqlDesignApi.md#put_sql_to_view_design) | **PUT** /api/Sql/toviewdesign | [EXPERIMENTAL] PutSqlToViewDesign: Generates a structured view creation design from existing view creation SQL.
*SqlDesignApi* | [**put_sql_to_writer_design**](docs/SqlDesignApi.md#put_sql_to_writer_design) | **PUT** /api/Sql/towriterdesign | [EXPERIMENTAL] PutSqlToWriterDesign: Generates a SQL-writer-design object from SQL string, if possible.
*SqlDesignApi* | [**put_view_design_to_sql**](docs/SqlDesignApi.md#put_view_design_to_sql) | **PUT** /api/Sql/fromviewdesign | [EXPERIMENTAL] PutViewDesignToSql: Generates view creation sql from a structured view creation design
*SqlDesignApi* | [**put_writer_design_to_sql**](docs/SqlDesignApi.md#put_writer_design_to_sql) | **PUT** /api/Sql/fromwriterdesign | [EXPERIMENTAL] PutWriterDesignToSql: Generates writer SQL from a valid writer-design structure
*SqlExecutionApi* | [**get_by_query_csv**](docs/SqlExecutionApi.md#get_by_query_csv) | **GET** /api/Sql/csv/{query} | GetByQueryCsv: Executes Sql, returned in CSV format, where the sql is simply in the url.
*SqlExecutionApi* | [**get_by_query_excel**](docs/SqlExecutionApi.md#get_by_query_excel) | **GET** /api/Sql/excel/{query} | GetByQueryExcel: Executes Sql, returned in Excel (xlsx) format (as a file to be downloaded) format, where the sql is simply in the url.
*SqlExecutionApi* | [**get_by_query_json**](docs/SqlExecutionApi.md#get_by_query_json) | **GET** /api/Sql/json/{query} | GetByQueryJson: Executes Sql, returned in JSON format, where the sql is simply in the url.
*SqlExecutionApi* | [**get_by_query_parquet**](docs/SqlExecutionApi.md#get_by_query_parquet) | **GET** /api/Sql/parquet/{query} | GetByQueryParquet: Executes Sql, returned in Parquet (.parquet) format (as a file to be downloaded) format, where the sql is simply in the url.
*SqlExecutionApi* | [**get_by_query_pipe**](docs/SqlExecutionApi.md#get_by_query_pipe) | **GET** /api/Sql/pipe/{query} | GetByQueryPipe: Executes Sql, returned in pipe-delimited format, where the sql is simply in the url.
*SqlExecutionApi* | [**get_by_query_sqlite**](docs/SqlExecutionApi.md#get_by_query_sqlite) | **GET** /api/Sql/sqlite/{query} | GetByQuerySqlite: Executes Sql, returned in SqLite DB (sqlite3) format (as a file to be downloaded) format, where the sql is simply in the url.
*SqlExecutionApi* | [**get_by_query_xml**](docs/SqlExecutionApi.md#get_by_query_xml) | **GET** /api/Sql/xml/{query} | GetByQueryXml: Executes Sql, returned in Xml format, where the sql is simply in the url.
*SqlExecutionApi* | [**put_by_query_csv**](docs/SqlExecutionApi.md#put_by_query_csv) | **PUT** /api/Sql/csv | PutByQueryCsv: Executes Sql, returned in CSV format, where the sql is the post-body url.
*SqlExecutionApi* | [**put_by_query_excel**](docs/SqlExecutionApi.md#put_by_query_excel) | **PUT** /api/Sql/excel | PutByQueryExcel: Executes Sql, returned in Excel (xlsx) format (as a file to be downloaded), where the sql is the post-body url.
*SqlExecutionApi* | [**put_by_query_json**](docs/SqlExecutionApi.md#put_by_query_json) | **PUT** /api/Sql/json | PutByQueryJson: Executes Sql, returned in JSON format, where the sql is the post-body url.
*SqlExecutionApi* | [**put_by_query_parquet**](docs/SqlExecutionApi.md#put_by_query_parquet) | **PUT** /api/Sql/parquet | PutByQueryParquet: Executes Sql, returned in Parquet format, where the sql is the post-body url.
*SqlExecutionApi* | [**put_by_query_pipe**](docs/SqlExecutionApi.md#put_by_query_pipe) | **PUT** /api/Sql/pipe | PutByQueryPipe: Executes Sql, returned in pipe-delimited format, where the sql is the post-body url.
*SqlExecutionApi* | [**put_by_query_sqlite**](docs/SqlExecutionApi.md#put_by_query_sqlite) | **PUT** /api/Sql/sqlite | PutByQuerySqlite: Executes Sql, returned in SqLite DB (sqlite3) format (as a file to be downloaded), where the sql is the post-body url.
*SqlExecutionApi* | [**put_by_query_xml**](docs/SqlExecutionApi.md#put_by_query_xml) | **PUT** /api/Sql/xml | PutByQueryXml: Executes Sql, returned in Xml format, where the sql is the post-body url.


<a id="documentation-for-models"></a>
## Documentation for Models

 - [AccessControlledAction](docs/AccessControlledAction.md)
 - [AccessControlledResource](docs/AccessControlledResource.md)
 - [AccessControlledResourceIdentifierPartSchemaAttribute](docs/AccessControlledResourceIdentifierPartSchemaAttribute.md)
 - [ActionId](docs/ActionId.md)
 - [AggregateFunction](docs/AggregateFunction.md)
 - [Aggregation](docs/Aggregation.md)
 - [AutoDetectType](docs/AutoDetectType.md)
 - [AvailableField](docs/AvailableField.md)
 - [AvailableParameter](docs/AvailableParameter.md)
 - [BackgroundMultiQueryProgressResponse](docs/BackgroundMultiQueryProgressResponse.md)
 - [BackgroundMultiQueryResponse](docs/BackgroundMultiQueryResponse.md)
 - [BackgroundQueryCancelResponse](docs/BackgroundQueryCancelResponse.md)
 - [BackgroundQueryProgressResponse](docs/BackgroundQueryProgressResponse.md)
 - [BackgroundQueryResponse](docs/BackgroundQueryResponse.md)
 - [BackgroundQueryState](docs/BackgroundQueryState.md)
 - [CaseStatementDesign](docs/CaseStatementDesign.md)
 - [CaseStatementItem](docs/CaseStatementItem.md)
 - [CertificateAction](docs/CertificateAction.md)
 - [CertificateFileType](docs/CertificateFileType.md)
 - [CertificateState](docs/CertificateState.md)
 - [CertificateStatus](docs/CertificateStatus.md)
 - [CertificateType](docs/CertificateType.md)
 - [Column](docs/Column.md)
 - [ColumnInfo](docs/ColumnInfo.md)
 - [ConditionAttributes](docs/ConditionAttributes.md)
 - [ConvertToViewData](docs/ConvertToViewData.md)
 - [CursorPosition](docs/CursorPosition.md)
 - [DataType](docs/DataType.md)
 - [ErrorHighlightItem](docs/ErrorHighlightItem.md)
 - [ErrorHighlightRequest](docs/ErrorHighlightRequest.md)
 - [ErrorHighlightResponse](docs/ErrorHighlightResponse.md)
 - [ExpressionWithAlias](docs/ExpressionWithAlias.md)
 - [FeedbackEventArgs](docs/FeedbackEventArgs.md)
 - [FeedbackLevel](docs/FeedbackLevel.md)
 - [FieldDesign](docs/FieldDesign.md)
 - [FieldType](docs/FieldType.md)
 - [FileReaderBuilderDef](docs/FileReaderBuilderDef.md)
 - [FileReaderBuilderResponse](docs/FileReaderBuilderResponse.md)
 - [FilterTermDesign](docs/FilterTermDesign.md)
 - [IdSelectorDefinition](docs/IdSelectorDefinition.md)
 - [InlinedPropertyDesign](docs/InlinedPropertyDesign.md)
 - [InlinedPropertyItem](docs/InlinedPropertyItem.md)
 - [IntellisenseItem](docs/IntellisenseItem.md)
 - [IntellisenseRequest](docs/IntellisenseRequest.md)
 - [IntellisenseResponse](docs/IntellisenseResponse.md)
 - [IntellisenseType](docs/IntellisenseType.md)
 - [Link](docs/Link.md)
 - [LuminesceBinaryType](docs/LuminesceBinaryType.md)
 - [LusidProblemDetails](docs/LusidProblemDetails.md)
 - [MappableField](docs/MappableField.md)
 - [MappingFlags](docs/MappingFlags.md)
 - [MultiQueryDefinitionType](docs/MultiQueryDefinitionType.md)
 - [OptionsCsv](docs/OptionsCsv.md)
 - [OptionsExcel](docs/OptionsExcel.md)
 - [OptionsParquet](docs/OptionsParquet.md)
 - [OptionsSqLite](docs/OptionsSqLite.md)
 - [OptionsXml](docs/OptionsXml.md)
 - [OrderByDirection](docs/OrderByDirection.md)
 - [OrderByTermDesign](docs/OrderByTermDesign.md)
 - [QueryDesign](docs/QueryDesign.md)
 - [QueryDesignerBinaryOperator](docs/QueryDesignerBinaryOperator.md)
 - [ResourceListOfAccessControlledResource](docs/ResourceListOfAccessControlledResource.md)
 - [ScalarParameter](docs/ScalarParameter.md)
 - [Source](docs/Source.md)
 - [SourceType](docs/SourceType.md)
 - [TaskStatus](docs/TaskStatus.md)
 - [ViewParameter](docs/ViewParameter.md)
 - [WriterDesign](docs/WriterDesign.md)

