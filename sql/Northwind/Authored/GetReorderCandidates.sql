CREATE PROCEDURE [dbo].[GetReorderCandidates]
AS
BEGIN
    SET NOCOUNT ON;

    WITH candidates AS (
        SELECT
            p.[ProductID],
            p.[ProductName],
            p.[Discontinued],
            ISNULL(CONVERT(INT, p.[ReorderLevel]), 0) - (
                ISNULL(CONVERT(INT, p.[UnitsInStock]), 0) + ISNULL(CONVERT(INT, p.[UnitsOnOrder]), 0)
            ) AS [Shortage]
        FROM [dbo].[Products] AS p
    )

    SELECT
        c.[ProductID],
        c.[ProductName],
        c.[Shortage]
    FROM candidates AS c
    WHERE c.[Discontinued] = 0 AND c.[Shortage] > 0
    ORDER BY c.[ProductID] ASC;
END;
GO
