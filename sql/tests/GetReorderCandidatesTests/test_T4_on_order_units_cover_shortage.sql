CREATE PROCEDURE [GetReorderCandidatesTests].[test T4 on order units cover shortage] -- noqa: RF05
AS
BEGIN
    SET NOCOUNT ON;
    EXEC [tSQLt].[FakeTable] @TableName = N'dbo.Products';

    INSERT INTO [dbo].[Products] (
        [ProductID], [ProductName], [Discontinued], [ReorderLevel], [UnitsInStock], [UnitsOnOrder]
    )
    VALUES
    (1, N'Covered by orders', 0, 10, 4, 6);

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
