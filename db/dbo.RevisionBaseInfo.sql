CREATE TABLE dbo.RevisionBaseInfo
	(
	Id nvarchar(50) NOT NULL,
	Author nvarchar(50) NULL,
	Date datetime NULL,
	isFilesProcceed bit,
	primary key (Id)
	) 
