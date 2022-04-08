-- Part (a)
CREATE TABLE InsuranceCo (
    name varchar(50) PRIMARY KEY,
    phone int
);



CREATE TABLE Person (
    ssn int PRIMARY KEY,
    name varchar(50)
);



CREATE TABLE Driver (
    ssn int PRIMARY KEY REFERENCES Person(ssn),
    driverID int
);



CREATE TABLE NonProfessionalDriver (
    ssn int PRIMARY KEY REFERENCES Driver(ssn)
);



CREATE TABLE ProfessionalDriver (
    ssn int PRIMARY KEY REFERENCES Driver(ssn),
    medicalHistory varchar(100)
);



CREATE TABLE Vehicle (
    licensePlate varchar(10) PRIMARY KEY,
    year int,
    maxLiability real,
    insuranceCompany varchar(50) REFERENCES InsuranceCo(name),
    owner int REFERENCES Person(ssn)
);



CREATE TABLE Truck (
    licensePlate varchar(10) PRIMARY KEY REFERENCES Vehicle(licensePlate),
    capacity int,
    operatorssn int REFERENCES ProfessionalDriver(ssn)
);



CREATE TABLE Car (
    licensePlate varchar(10) PRIMARY KEY REFERENCES Vehicle(licensePlate),
    make varchar(50)
);



CREATE TABLE Drives (
    carLicensePlate varchar(10) REFERENCES Car(licensePlate),
    driverssn int REFERENCES NonProfessionalDriver(ssn),
    PRIMARY KEY (carLicensePlate, driverssn)
);





-- Part (b)
/*
To represent the "insures" relationship, I use a column called "insuranceCompany"
in the Vehicle table as a foreign key referring to the "name" column in the table
InsuranceCo. This is a valid way to represent a relationship since we have a
many-to-one relationship here, that is, an insurance company can insures multiple
vehicles, while a vehicle can only be insured by at most one single insurance company,
and such a many-to-one "insures" relationship can be stored in the Vehicle table as a
foreign key without the need to create an extra table.
*/




-- Part (c)
/*
Since "operates" is a many-to-one relationship, as above, we can use a column in
the truck table as a reference to the ssn of a professional driver since a truck
can only be operated by at most one single professional driver so that we don't have to
create an extra table.

While "drives" is a many-to-many relationship. In this case, we need both a
non-professional driver's ssn and a car's license plate to keep a relationship.
Thus, we have to create an extra table called "Drives" and use the combination
of ssn and license plate as the primary key to find a specific instance.
*/