CREATE PROCEDURE [GetReorderCandidatesTests].[test T6 numeric nulls treated as zero] -- noqa: RF05
AS
BEGIN
    SET NOCOUNT ON;
    EXEC [tSQLt].[FakeTable] @TableName = N'dbo.Products';

    INSERT INTO [dbo].[Products] (
        [ProductID], [ProductName], [Discontinued], [ReorderLevel], [UnitsInStock], [UnitsOnOrder]
    )
    VALUES
    (1, N'Null stock', 0, 10, NULL, 2),
    (2, N'Null orders', 0, 10, 4, NULL),
    (3, N'Null stock and orders', 0, 10, NULL, NULL),
    (4, N'Null threshold', 0, NULL, 4, 2),
    (5, N'Null threshold and stock', 0, NULL, NULL, 2),
    (6, N'Null threshold and orders', 0, NULL, 4, NULL),
    (7, N'All numeric nulls', 0, NULL, NULL, NULL);

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
    (1, N'Null stock', 8),
    (2, N'Null orders', 6),
    (3, N'Null stock and orders', 10);

    INSERT INTO #actual ([ProductID], [ProductName], [Shortage])
    EXEC [dbo].[GetReorderCandidates];

    EXEC [tSQLt].[AssertEqualsTable] @Expected = N'#expected', @Actual = N'#actual';
END;
GO
