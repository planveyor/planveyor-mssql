CREATE PROCEDURE [GetReorderCandidatesTests].[test T5 discontinued products excluded] -- noqa: RF05
AS
BEGIN
    SET NOCOUNT ON;
    EXEC [tSQLt].[FakeTable] @TableName = N'dbo.Products';

    INSERT INTO [dbo].[Products] (
        [ProductID], [ProductName], [Discontinued], [ReorderLevel], [UnitsInStock], [UnitsOnOrder]
    )
    VALUES
    (1, N'Discontinued shortage', 1, 10, 4, 2);

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
