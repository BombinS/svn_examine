--/****** Script for SelectTopNRows command from SSMS  ******/
--SELECT *
--  FROM [MC21].[dbo].[RevisionFileInfo] fi 
--  join [MC21].[dbo].[RevisionBaseInfo] ri on fi.revision = ri.Id
--  where extension = 'csv' and path like '%IVVPr_FWA/Tests/Developing/Testing_Procedures_for_SCADE%'
--  order by ri.Date desc


/****** Script for SelectTopNRows command from SSMS  ******/
--SELECT distinct (filename) 
--  FROM [MC21].[dbo].[RevisionFileInfo]
--  where extension = 'csv' and path like '%IVVPr_FWA/Tests/Developing/Testing_Procedures_for_SCADE%'

SELECT fi.revision, fi.path, ri.Date, ri.Author 
  FROM [MC21].[dbo].[RevisionFileInfo] fi 
  join [MC21].[dbo].[RevisionBaseInfo] ri on fi.revision = ri.Id
  where extension = 'csv' and path like '%IVVPr_FWA/Tests/Developing/Testing_Procedures_for_SCADE%' and filename = 'MC21_FWA_LOC_RESET_50'
  order by ri.Date desc

