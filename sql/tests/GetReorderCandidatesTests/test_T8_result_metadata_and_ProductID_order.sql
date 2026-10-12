CREATE PROCEDURE [GetReorderCandidatesTests].[test T8 result metadata and ProductID order] -- noqa: RF05
AS
BEGIN
    SET NOCOUNT ON;
    EXEC [tSQLt].[FakeTable] @TableName = N'dbo.Products';

    INSERT INTO [dbo].[Products] (
        [ProductID], [ProductName], [Discontinued], [ReorderLevel], [UnitsInStock], [UnitsOnOrder]
    )
    VALUES
    (30, N'Late product', 0, 10, 4, 2),
    (2, N'Early product', 0, 12, 1, 3),
    (11, N'Middle product', 0, 7, 1, 1);

    DECLARE @procedure_id INT = OBJECT_ID(N'dbo.GetReorderCandidates', N'P');
    IF @procedure_id IS NULL
        BEGIN
            EXEC [tSQLt].[Fail] N'GetReorderCandidates must be a SQL procedure';
        END;

    SELECT
        is_hidden,
        column_ordinal,
        [name],
        system_type_name,
        ordinal_in_order_by_list,
        order_by_is_descending,
        order_by_list_length,
        error_number,
        error_type
    INTO #metadata
    FROM sys.dm_exec_describe_first_result_set_for_object(@procedure_id, 0);

    DECLARE @metadata_errors INT;
    SELECT @metadata_errors = COUNT(*)
    FROM #metadata
    WHERE error_number IS NOT NULL OR error_type IS NOT NULL OR is_hidden IS NULL;

    IF @metadata_errors > 0
        BEGIN
            EXEC [tSQLt].[Fail] N'Result metadata must be determinable without errors';
        END;

    CREATE TABLE #expected_metadata (
        column_ordinal INT,
        [name] NVARCHAR(128),
        system_type_name NVARCHAR(256),
        ordinal_in_order_by_list SMALLINT,
        order_by_is_descending SMALLINT,
        order_by_list_length SMALLINT
    );
    INSERT INTO #expected_metadata (
        column_ordinal,
        [name],
        system_type_name,
        ordinal_in_order_by_list,
        order_by_is_descending,
        order_by_list_length
    )
    VALUES
    (1, N'ProductID', N'int', 1, 0, 1),
    (2, N'ProductName', N'nvarchar(40)', NULL, NULL, 1),
    (3, N'Shortage', N'int', NULL, NULL, 1);

    SELECT
        column_ordinal,
        [name],
        system_type_name,
        ordinal_in_order_by_list,
        order_by_is_descending,
        order_by_list_length
    INTO #actual_metadata
    FROM #metadata
    WHERE is_hidden = 0;

    EXEC [tSQLt].[AssertEqualsTable]
        @Expected = N'#expected_metadata',
        @Actual = N'#actual_metadata';

    CREATE TABLE #actual (
        [ProductID] INT,
        [ProductName] NVARCHAR(40),
        [Shortage] INT
    );
    CREATE TABLE #expected (
        [ProductID] INT,
        [ProductName] NVARCHAR(40),
        [Shortage] INT
    );

    INSERT INTO #expected ([ProductID], [ProductName], [Shortage])
    VALUES
    (2, N'Early product', 8),
    (11, N'Middle product', 5),
    (30, N'Late product', 4);

    INSERT INTO #actual ([ProductID], [ProductName], [Shortage])
    EXEC [dbo].[GetReorderCandidates];

    EXEC [tSQLt].[AssertEqualsTable] @Expected = N'#expected', @Actual = N'#actual';
END;
GO
