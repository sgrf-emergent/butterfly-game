-- ============================================
-- Butterfly Identification App - Seed Data
-- 30 Butterfly Species with Images
-- ============================================

USE butterfly_app;

-- Clear existing data (optional - comment out if you want to preserve data)
-- TRUNCATE TABLE scores;
-- TRUNCATE TABLE butterflies;

-- ============================================
-- Insert 30 Butterfly Species
-- Difficulty: 1 = Easy, 2 = Medium, 3 = Hard
-- ============================================

INSERT INTO butterflies (commonName, latinName, imageUrl, difficulty) VALUES
-- Easy Butterflies (difficulty = 1)
('Monarch', 'Danaus plexippus', 'https://images.unsplash.com/photo-1560263816-d704d83cce0f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwxfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85', 1),
('Painted Lady', 'Vanessa cardui', 'https://images.unsplash.com/photo-1533048324814-79b0a31982f1?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwzfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85', 1),
('Red Admiral', 'Vanessa atalanta', 'https://images.unsplash.com/photo-1564514476902-542f8c30121e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHw0fHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85', 1),
('Tiger Swallowtail', 'Papilio glaucus', 'https://images.unsplash.com/photo-1702338354821-0ea4fb0221e3?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85', 1),
('Black Swallowtail', 'Papilio polyxenes', 'https://images.unsplash.com/photo-1657244670691-ec73025cf69e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwyfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85', 1),
('Common Buckeye', 'Junonia coenia', 'https://images.unsplash.com/photo-1623615412998-c63b6d5fe9be?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85', 1),
('Cabbage White', 'Pieris rapae', 'https://images.unsplash.com/photo-1702338354821-0ea4fb0221e3?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwxfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85', 1),

-- Medium Butterflies (difficulty = 2)
('Blue Morpho', 'Morpho menelaus', 'https://images.unsplash.com/photo-1599631438215-75bc2640feb8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwyfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85', 2),
('Zebra Swallowtail', 'Eurytides marcellus', 'https://images.pexels.com/photos/2671074/pexels-photo-2671074.jpeg', 2),
('Mourning Cloak', 'Nymphalis antiopa', 'https://images.unsplash.com/photo-1592861377549-3586948b6a74?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHw0fHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85', 2),
('Viceroy', 'Limenitis archippus', 'https://images.pexels.com/photos/28749528/pexels-photo-28749528.jpeg', 2),
('Gulf Fritillary', 'Agraulis vanillae', 'https://images.unsplash.com/photo-1560263816-d704d83cce0f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwxfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85', 2),
('Clouded Sulphur', 'Colias philodice', 'https://images.unsplash.com/photo-1728946737947-3e1908c3750a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwzfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85', 2),
('Orange Sulphur', 'Colias eurytheme', 'https://images.unsplash.com/photo-1628181150173-f5f355d15f28?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85', 2),
('Cloudless Sulphur', 'Phoebis sennae', 'https://images.unsplash.com/photo-1564514476902-542f8c30121e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHw0fHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85', 2),
('American Lady', 'Vanessa virginiensis', 'https://images.unsplash.com/photo-1623615412998-c63b6d5fe9be?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85', 2),
('Spring Azure', 'Celastrina ladon', 'https://images.pexels.com/photos/2671074/pexels-photo-2671074.jpeg', 2),
('Little Yellow', 'Pyrisitia lisa', 'https://images.unsplash.com/photo-1657244670691-ec73025cf69e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwyfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85', 2),

-- Hard Butterflies (difficulty = 3)
('Spicebush Swallowtail', 'Papilio troilus', 'https://images.unsplash.com/photo-1728946737947-3e1908c3750a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHwzfHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85', 3),
('Pipevine Swallowtail', 'Battus philenor', 'https://images.unsplash.com/photo-1628181150173-f5f355d15f28?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njd8MHwxfHNlYXJjaHw0fHxzd2FsbG93dGFpbHxlbnwwfHx8fDE3NjMwMzM3ODl8MA&ixlib=rb-4.1.0&q=85', 3),
('Pearl Crescent', 'Phyciodes tharos', 'https://images.unsplash.com/photo-1484704193309-27eaa53936a7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwyfHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85', 3),
('Question Mark', 'Polygonia interrogationis', 'https://images.unsplash.com/photo-1509715513011-e394f0cb20c4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85', 3),
('Great Spangled Fritillary', 'Speyeria cybele', 'https://images.unsplash.com/photo-1533048324814-79b0a31982f1?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwzfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85', 3),
('Eastern Comma', 'Polygonia comma', 'https://images.unsplash.com/photo-1599631438215-75bc2640feb8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwyfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85', 3),
('Common Checkered-Skipper', 'Pyrgus communis', 'https://images.unsplash.com/photo-1484704193309-27eaa53936a7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwyfHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85', 3),
('Silver-spotted Skipper', 'Epargyreus clarus', 'https://images.unsplash.com/photo-1509715513011-e394f0cb20c4?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85', 3),
('Gray Hairstreak', 'Strymon melinus', 'https://images.unsplash.com/photo-1592861377549-3586948b6a74?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHw0fHxtb25hcmNofGVufDB8fHx8MTc2MzAzMzc4NHww&ixlib=rb-4.1.0&q=85', 3),
('Eastern Tailed-Blue', 'Cupido comyntas', 'https://images.pexels.com/photos/28749528/pexels-photo-28749528.jpeg', 3),
('Hackberry Emperor', 'Asterocampa celtis', 'https://images.unsplash.com/photo-1560263816-d704d83cce0f?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwxfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85', 3),
('Red-spotted Purple', 'Limenitis arthemis', 'https://images.unsplash.com/photo-1599631438215-75bc2640feb8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1Nzd8MHwxfHNlYXJjaHwyfHxidXR0ZXJmbHl8ZW58MHx8fHwxNzYzMDMzNzUzfDA&ixlib=rb-4.1.0&q=85', 3);

-- ============================================
-- Verify Data Insertion
-- ============================================
SELECT 
    difficulty,
    COUNT(*) as count,
    CASE difficulty
        WHEN 1 THEN 'Easy'
        WHEN 2 THEN 'Medium'
        WHEN 3 THEN 'Hard'
    END as level
FROM butterflies
GROUP BY difficulty
ORDER BY difficulty;

SELECT 'Total butterflies inserted:' as Status, COUNT(*) as Count FROM butterflies;
