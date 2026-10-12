CREATE PROCEDURE [GetReorderCandidatesTests].[test T7 smallint arithmetic does not overflow] -- noqa: RF05
AS
BEGIN
    SET NOCOUNT ON;
    EXEC [tSQLt].[FakeTable] @TableName = N'dbo.Products';

    INSERT INTO [dbo].[Products] (
        [ProductID], [ProductName], [Discontinued], [ReorderLevel], [UnitsInStock], [UnitsOnOrder]
    )
    VALUES
    (1, N'Maximum smallints', 0, 32767, 32767, 32767);

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

    INSERT INTO #actual ([ProductID], [ProductName], [Shortage])
    EXEC [dbo].[GetReorderCandidates];

    EXEC [tSQLt].[AssertEqualsTable] @Expected = N'#expected', @Actual = N'#actual';
END;
GO
