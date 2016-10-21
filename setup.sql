-- Dangerous Classes
INSERT INTO danger_classes (`name`) VALUES ('none');
INSERT INTO danger_classes (`name`) VALUES ('explosives');
INSERT INTO danger_classes (`name`) VALUES ('gases');
INSERT INTO danger_classes (`name`) VALUES ('flammable');
INSERT INTO danger_classes (`name`) VALUES ('oxidizing');
INSERT INTO danger_classes (`name`) VALUES ('toxic');
INSERT INTO danger_classes (`name`) VALUES ('corrosives');
INSERT INTO danger_classes (`name`) VALUES ('misc');

-- Service Types
INSERT INTO service_types (`name`) VALUES ('standard');
INSERT INTO service_types (`name`) VALUES ('express');
INSERT INTO service_types (`name`) VALUES ('overnight');
INSERT INTO service_types (`name`) VALUES ('dangerous');

-- Roles
INSERT INTO roles (`role_name`) VALUES ('user');
INSERT INTO roles (`role_name`) VALUES ('driver');
INSERT INTO roles (`role_name`) VALUES ('admin');