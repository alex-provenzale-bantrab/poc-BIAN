DROP TABLE IF EXISTS PartyState;
DROP TABLE IF EXISTS Status;
DROP TABLE IF EXISTS CustomerRelationshipStatusValidFromToDate;
DROP TABLE IF EXISTS Rating;
DROP TABLE IF EXISTS CustomerRelationshipRatingValidFromToDate;
DROP TABLE IF EXISTS Alert;
DROP TABLE IF EXISTS CustomerRelationshipAlertValidFromToDate;

CREATE TABLE PartyState (
    PartyStateId INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerReference VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE CustomerRelationshipStatusValidFromToDate (
    CustomerRelationshipStatusValidFromToDateId INTEGER PRIMARY KEY AUTOINCREMENT,
    DateContent VARCHAR(255) NOT NULL
);

CREATE TABLE Status (
    StatusId INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerRelationshipStatusType VARCHAR(255) NOT NULL,
    CustomerRelationshipStatusNarrative VARCHAR(255) NOT NULL,
    CustomerRelationshipStatusValidFromToDateId INTEGER NOT NULL,
    PartyStateId INTEGER NOT NULL,
    FOREIGN KEY (CustomerRelationshipStatusValidFromToDateId)
    REFERENCES CustomerRelationshipStatusValidFromToDate(CustomerRelationshipStatusValidFromToDateId)
    FOREIGN KEY (PartyStateId)
    REFERENCES PartyState(PartyStateId)
);

CREATE TABLE CustomerRelationshipRatingValidFromToDate (
    CustomerRelationshipRatingValidFromToDateId INTEGER PRIMARY KEY AUTOINCREMENT,
    DateContent VARCHAR(255) NOT NULL
);

CREATE TABLE Rating (
    RatingId INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerRelationshipRatingType VARCHAR(255) NOT NULL,
    CustomerRelationshipRatingNarrative VARCHAR(255) NOT NULL,
    CustomerRelationshipRatingValidFromToDateId INTEGER NOT NULL,
    PartyStateId INTEGER NOT NULL,
    FOREIGN KEY (CustomerRelationshipRatingValidFromToDateId)
    REFERENCES CustomerRelationshipRatingValidFromToDate(CustomerRelationshipRatingValidFromToDateId)
    FOREIGN KEY (PartyStateId)
    REFERENCES PartyState(PartyStateId)
);

CREATE TABLE CustomerRelationshipAlertValidFromToDate (
    CustomerRelationshipAlertValidFromToDateId INTEGER PRIMARY KEY AUTOINCREMENT,
    DateContent VARCHAR(255) NOT NULL
);

CREATE TABLE Alert (
    AlertId INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerRelationshipAlertType VARCHAR(255) NOT NULL,
    CustomerRelationshipAlertNarrative VARCHAR(255) NOT NULL,
    CustomerRelationshipAlertValidFromToDateId INTEGER NOT NULL,
    PartyStateId INTEGER NOT NULL,
    FOREIGN KEY (CustomerRelationshipAlertValidFromToDateId)
    REFERENCES CustomerRelationshipAlertValidFromToDate(CustomerRelationshipAlertValidFromToDateId)
    FOREIGN KEY (PartyStateId)
    REFERENCES PartyState(PartyStateId)
);
