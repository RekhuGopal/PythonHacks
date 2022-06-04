CREATE TABLE IF NOT EXISTS package (
    package_name VARCHAR(100) NOT NULL,
    package_version VARCHAR(50) NOT NULL,
    PRIMARY KEY (package_name, package_version)
)
