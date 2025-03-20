-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: musicfinder
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `albumes`
--

DROP TABLE IF EXISTS `albumes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `albumes` (
  `id_album` varchar(255) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `artista` varchar(255) NOT NULL,
  `year` int DEFAULT NULL,
  `formato` varchar(100) DEFAULT NULL,
  `url` varchar(500) DEFAULT NULL,
  `sello_discografico` text,
  `rating` float DEFAULT NULL,
  `lastfm_listeners` int DEFAULT NULL,
  `lastfm_plays` int DEFAULT NULL,
  `lastfm_url` varchar(500) DEFAULT NULL,
  `lastfm_image` varchar(500) DEFAULT NULL,
  `lastfm_tags` varchar(500) DEFAULT NULL,
  `discogs_availability` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id_album`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `albumes`
--

LOCK TABLES `albumes` WRITE;
/*!40000 ALTER TABLE `albumes` DISABLE KEYS */;
INSERT INTO `albumes` VALUES ('10002496','Pierre Boulez - The Complete Columbia Album Collection','Christian Wünsch',2014,'CD, Compilation, Remastered, Box Set','https://api.discogs.com/releases/10002496','Sony Classical, Sony Music Entertainment, Sony Music Entertainment, Sony Music Entertainment, Boosey & Hawkes, Universal Edition, Theodore Presser, Belmont Music, Chester Music Ltd., G. Schirmer Inc., Max Eschig, Colfranc Music Publishing Corporation, European American Music Distributors Corporation, Associated Music Publishers, C. F. Peters, Alexander Broude, Inc., Verlag Dreililien, Schott Music, Hendon Music, Bote & Bock, Israeli Music Publications, Maison de la Mutualité, Notre-Dame du Liban, Barking Town Hall, Walthamstow Assembly Hall, Severance Hall, Abbey Road Studios, Avery Fisher Hall, Studio Davout, Manhattan Center, West Ham Central Mission, London, Columbia 30th Street Studio, Kingsway Hall, Olympic Studios, CBS Studios, London, Espace de projection, Ircam, Henry Wood Hall, London, St. John\'s, Smith Square, Weinbrennersaal Baden-Baden, Maida Vale Studios, Watford Town Hall, Concordia College, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC, Sony DADC',NULL,NULL,NULL,NULL,NULL,NULL,1),('1015465','Led Zeppelin - Led Zeppelin IV','Led Zeppelin',1978,'Vinyl, LP, Album, Reissue, Stereo','https://api.discogs.com/releases/1015465','Atlantic, Warner Communications, Atlantic Recording Corporation, WEA Italiana S.p.A., WEA Italiana S.p.A., Graphreaks, Superhype Music, Headley Grange, Sunset Sound Recorders',NULL,107570,1949623,'https://www.last.fm/music/Led+Zeppelin/IV','https://lastfm.freetls.fastly.net/i/u/300x300/56b6e759db3949c5a36bd62f5ff30f49.png','hard rock, classic rock, rock, 70s, 1971',1),('10598780','Various - 3 Years Of Faut Section','Lewis Fautzi',2017,'CD, Compilation','https://api.discogs.com/releases/10598780','Faut Section',NULL,NULL,NULL,NULL,NULL,NULL,1),('11463891','Oscar Mulero - Acceptance','Oscar Mulero',2018,'Vinyl, 12\", EP','https://api.discogs.com/releases/11463891','Semantica Records',NULL,163,1944,'https://www.last.fm/music/Oscar+Mulero/Acceptance','https://lastfm.freetls.fastly.net/i/u/300x300/4e15deb8307cea6eced1aeb0ee7099ec.jpg','techno, minimal techno, electronic, hard techno, minimal',1),('11665040','Exium - Expect Nothing Remixes','Exium',2018,'Vinyl, 12\", 33 ⅓ RPM','https://api.discogs.com/releases/11665040','Nheoma, Nheoma, Nheoma, The Exchange Vinyl, Record Industry, Triple Vision Record Distribution',NULL,NULL,NULL,NULL,NULL,NULL,1),('11753908','Oscar Mulero - Perfect Peace','Oscar Mulero',2018,'Vinyl, 12\", Album','https://api.discogs.com/releases/11753908','Semantica Records, Dead Souls Studio, Koschitzky Mastering, Record Industry',NULL,289,7601,'https://www.last.fm/music/Oscar+Mulero/Perfect+Peace','https://lastfm.freetls.fastly.net/i/u/300x300/db8ec28627e50d45465e4726ee271862.png','',1),('12347','Regis - Penetration','Regis',2001,'Vinyl, 12\", 33 ⅓ RPM, Album','https://api.discogs.com/releases/12347','Downwards, MPO, The Exchange, Downwards, Downwards',NULL,920,15552,'https://www.last.fm/music/Regis/Penetration','https://lastfm.freetls.fastly.net/i/u/300x300/509a5afedaed6e83aff50b8b971bd001.png','techno, industrial, industrial techno, electronic, downtempo',1),('12521351','Lewis Fautzi - Deep Illusion','Lewis Fautzi',2018,'Vinyl, 12\"','https://api.discogs.com/releases/12521351','BPitch Control, BPitch Control Music Publishing, Eternal Midnight Mastering Studio',NULL,381,1416,'https://www.last.fm/music/Lewis+Fautzi/Deep+Illusion','https://lastfm.freetls.fastly.net/i/u/300x300/f8364c6fcf408f530529484cd58a5a28.png','techno, electronic, minimal, minimal techno, ambient',1),('14105','Surgeon - Balance','Surgeon',1998,'Vinyl, 12\", 33 ⅓ RPM, 45 RPM, Album','https://api.discogs.com/releases/14105','Tresor, Dynamic Tension Records, Tresor Records, Tresor Records, Interfisch Records, Copyright Control, Dubplates & Mastering, Schallplattenfabrik Pallas GmbH, EFA',NULL,12143,56613,'https://www.last.fm/music/Surgeon/Balance','https://lastfm.freetls.fastly.net/i/u/300x300/c2ad5bc3429ed7c0e38352ad01678d12.jpg','techno, minimal techno, 77davez-all-tracks, totec radio, adrien wayne',1),('14186441','The Beatles - Abbey Road','The Beatles',2019,'Vinyl, LP, Album, Reissue, Remastered, Stereo','https://api.discogs.com/releases/14186441','Apple Records, Universal Music Group International, Apple Records, Optimal Media GmbH, Optimal Media GmbH, Abbey Road Studios, Abbey Road Studios, Calderstone Productions Limited, Apple Corps Ltd., Calderstone Productions Limited, Apple Corps Ltd., Harrisongs Ltd., Sony/ATV Music Publishing LLC, Startling Music, BMG Platinum',NULL,1109050,44200894,'https://www.last.fm/music/The+Beatles/Abbey+Road','https://lastfm.freetls.fastly.net/i/u/300x300/f304ba0296794c6fc9d0e1cccd194ed0.jpg','rock, 1969, 60s, classic rock, pop',1),('1587168','Radiohead - OK Computer','Radiohead',2008,'Vinyl, LP, Album, Limited Edition, Reissue','https://api.discogs.com/releases/1587168','Capitol Records, From The Capitol Vaults, EMI Records Ltd., EMI Records Ltd., Canned Applause? Mobile, Abbey Road Studios, Mayfair Studios, Abbey Road Studios, Air Lyndhurst Hall, Courtyard Studio, The Church, London, Hubdesign, The Whole Hog, Warner Chappell Ltd., Capitol Records, LLC, Capitol Mastering, Rainbo Records, Rainbo Records, Rainbo Records, Rainbo Records',NULL,3826839,170962210,'https://www.last.fm/music/Radiohead/OK+Computer','https://lastfm.freetls.fastly.net/i/u/300x300/131e3e85d45047e93ab77b422e591719.jpg','alternative, alternative rock, rock, radiohead, indie',1),('1655444','Ben Klock - One','Ben Klock',2009,'Vinyl, 12\", 33 ⅓ RPM, Album','https://api.discogs.com/releases/1655444','Ostgut Ton, Ostgut Ton, Ostgut Ton, Kompakt Distribution, Dubplates & Mastering',NULL,12356,171029,'https://www.last.fm/music/Ben+Klock/One','https://lastfm.freetls.fastly.net/i/u/300x300/9501cee09cef4e86bb8652823c4fd824.png','techno, minimal techno, elektronischer-b0lzen, dub techno, minimal',1),('17518','Jeff Mills - Waveform Transmission Vol. 1','Jeff Mills',1993,'Vinyl, 12\", 33 ⅓ RPM, EP, Vinyl, 12\", 33 ⅓ RPM, EP, All Media, Album','https://api.discogs.com/releases/17518','Tresor, Interfisch Records, Axis Records, Tresor, Millsart, Millsart, The Exchange, EFA',NULL,4562,50734,'https://www.last.fm/music/Jeff+Mills/Waveform+Transmission+Vol.+1','https://lastfm.freetls.fastly.net/i/u/300x300/3f19b6918f724606a705bfe4ddc7c8dd.png','techno, detroit techno, detroit, 1992, industrial techno',1),('17566192','DVS1 - Beta Sensory Motor Rhythm','DVS1',2021,'Vinyl, 12\", 33 ⅓ RPM, Album','https://api.discogs.com/releases/17566192','HUSH, Axis Records, Manmade Mastering, Manmade Mastering',NULL,963,8000,'https://www.last.fm/music/DVS1/Beta+Sensory+Motor+Rhythm','https://lastfm.freetls.fastly.net/i/u/300x300/e939bd446b86af0d6357bb77c724ad74.jpg','techno, hard techno, minimal techno, electronic, minneapolis',1),('18315','Surgeon - Force + Form Remakes','Surgeon',1999,'Vinyl, 12\", 33 ⅓ RPM','https://api.discogs.com/releases/18315','Tresor, Tresor Records, Tresor Records, Interfisch Records, Copyright Control, Dubplates & Mastering, Schallplattenfabrik Pallas GmbH, EFA',NULL,8347,41840,'https://www.last.fm/music/Surgeon/Force+%252B+Form','https://lastfm.freetls.fastly.net/i/u/300x300/a5180286e250139f0c6f2c60473cdb11.png','techno, minimal techno, uk techno, musick, british techno',1),('2386','Robert Hood - Minimal Nation','Robert Hood',1994,'Vinyl, 12\", 33 ⅓ RPM, EP','https://api.discogs.com/releases/2386','Axis, M-Plant Studio, M-Plant Studio, Axis Records, Millsart, BMG Ariola, National Sound Corporation',NULL,31667,207279,'https://www.last.fm/music/Robert+Hood/Minimal+Nation','https://lastfm.freetls.fastly.net/i/u/300x300/042fedd873169884bfd7e4f0ea9d493c.png','techno, minimal techno, detroit techno, minimal, 1994',1),('244049','Robert Lamart - References (Various Artists)','Exium',2003,'CD, Album, Mixed','https://api.discogs.com/releases/244049','Mainout',NULL,NULL,NULL,NULL,NULL,NULL,1),('25942','Robert Hood - Internal Empire','Robert Hood',1994,'Vinyl, 12\", 45 RPM, Album','https://api.discogs.com/releases/25942','Tresor, Tresor, Logic Records, Logic Records, M-Plant Music, M-Plant Music, Logic Records, Millsart, BMG Ariola, M-Plant Studio, SST Brüggemann GmbH',NULL,9633,107510,'https://www.last.fm/music/Robert+Hood/Internal+Empire','https://lastfm.freetls.fastly.net/i/u/300x300/6fa09287b7ea8414ddfb8123d9f6a722.png','techno, 1994, minimal techno, detroit techno, minimal',1),('26752457','Various - Granulart Compilation #09','Oscar Mulero',2022,'File, WAV, Compilation','https://api.discogs.com/releases/26752457','Granulart Recordings',NULL,NULL,NULL,NULL,NULL,NULL,1),('2680826','Exium - Roots Of Time','Exium',2011,'Vinyl, 12\", 33 ⅓ RPM, Album','https://api.discogs.com/releases/2680826','Nheoma',NULL,274,2695,'https://www.last.fm/music/Exium/Roots+Of+Time','https://lastfm.freetls.fastly.net/i/u/300x300/b6f9760655ddaf8c9136de6a969962dd.jpg','techno, minimal techno, dark techno, hard techno, electronic',1),('2761591','Oscar Mulero - Grey Fades To Green','Oscar Mulero',2011,'Vinyl, 12\", Album','https://api.discogs.com/releases/2761591','Warm Up Recordings',NULL,3104,20932,'https://www.last.fm/music/Oscar+Mulero/Grey+Fades+To+Green','https://lastfm.freetls.fastly.net/i/u/300x300/fb657f53d97d4093c046aaec380fc4d1.jpg','techno, minimal techno, electronic, hard techno, minimal',1),('3188370','Reeko - Finding The New Matter','Reeko',2011,'Vinyl, 12\", 33 ⅓ RPM, Album','https://api.discogs.com/releases/3188370','Mental Disorder, Triple Vision Record Distribution, Record Industry',NULL,317,3182,'https://www.last.fm/music/Reeko/Finding+The+New+Matter','https://lastfm.freetls.fastly.net/i/u/300x300/45c9f964aa434eab97992154e3d56bb7.jpg','techno, minimal techno, industrial techno, experimental, dark techno',1),('34920','Speedy J - Loudboxer','Speedy J',2002,'Vinyl, 12\", 33 ⅓ RPM, Special Cut','https://api.discogs.com/releases/34920','NovaMute, NovaMute, Speedy J Music, Strictly Confidential, Mute Records Ltd., Mute Records Ltd., Vital, Dubplates & Mastering, MPO',NULL,13839,97573,'https://www.last.fm/music/Speedy+J/Loudboxer','https://lastfm.freetls.fastly.net/i/u/300x300/50abc4df5b451e5b906f3dc67a8d77f9.jpg','techno, electronic, dutch, cold, minimal',1),('3720024','Oscar Mulero - Black Propaganda','Oscar Mulero',2012,'Vinyl, 12\", Album','https://api.discogs.com/releases/3720024','Warm Up Recordings, Eternal Midnight Mastering Studio, Triple Vision Record Distribution, Record Industry',NULL,3510,27791,'https://www.last.fm/music/Oscar+Mulero/Black+Propaganda','https://lastfm.freetls.fastly.net/i/u/300x300/2501c398fadd49d6a730ceda80bccd98.jpg','techno, minimal techno, electronic, hard techno, minimal',1),('3834425','Various - The Structure EP','Christian Wünsch',2012,'Vinyl, 12\", 33 ⅓ RPM, EP','https://api.discogs.com/releases/3834425','Injected Poison Records, Triple Vision Record Distribution',NULL,NULL,NULL,NULL,NULL,NULL,1),('451342','The Rolling Stones - Sticky Fingers','The Rolling Stones',1971,'Vinyl, LP, Album','https://api.discogs.com/releases/451342','Rolling Stones Records, Philips Recording Company, Inc., ATCO Records, Sound Packaging Corp., Olympic Studios, Rolling Stones Mobile, Gideon Music, Inc., Musidor N.V.',NULL,566480,6334206,'https://www.last.fm/music/The+Rolling+Stones/Sticky+Fingers','https://lastfm.freetls.fastly.net/i/u/300x300/5ffc0e1908e44522c50a6e56300ec7ef.png','classic rock, rock, 70s, 1971, the rolling stones',1),('4570366','Daft Punk - Random Access Memories','Daft Punk',2013,'Vinyl, LP, Album, Stereo','https://api.discogs.com/releases/4570366','Columbia, Columbia, Sony Music, Sony Music Entertainment, Daft Life Ltd., Daft Life Ltd., Columbia Records, Sony Music Entertainment, Sony Music Entertainment Poland Sp. z o.o., Daft Punk, Imagem Music, Daft Music, Because Music, XLC Music, Miss Mittie Music, Giorgio Moroder Publishing Co., EMI Music Publishing, Julian Casablancas Publishing, Warner/Chappell Music Publishing Ltd., EMI April Music Inc., More Water From Nazareth, Sunset Squid Music, Kazz Song, Inc., Todd Imperatrice, Chrysalis, Stéphane Quême, Perfect Pitch Music Publishing, Liberation Music PTY Ltd., Rhino Entertainment Company, Warner Music Group, Studio Gang, Henson Recording Studios, Conway Studios, Electric Lady Studios, Capitol Studios, Conway Studios, Gateway Mastering, Translab, Optimal Media GmbH',NULL,2004294,68564505,'https://www.last.fm/music/Daft+Punk/Random+Access+Memories','https://lastfm.freetls.fastly.net/i/u/300x300/11dd7e48a1f042c688bf54985f01d088.png','electronic, disco, 2013, funk, house',1),('554869','Jeff Mills - Blade Runner','Jeff Mills',2005,'Vinyl, 12\", 33 ⅓ RPM','https://api.discogs.com/releases/554869','Axis, Axis, Millsart, Mikrofisch-BMG, National Sound Corporation',NULL,NULL,NULL,NULL,NULL,NULL,1),('5566646','Lewis Fautzi - The Gare Album','Lewis Fautzi',2014,'Vinyl, 12\", 33 ⅓ RPM, Album','https://api.discogs.com/releases/5566646','Soma Quality Recordings, Soma Recordings Ltd., Soma Recordings Ltd., SPG Publishing UK Ltd, Finyl Tweek, MPO',NULL,1981,12762,'https://www.last.fm/music/Lewis+Fautzi/The+Gare+Album','https://lastfm.freetls.fastly.net/i/u/300x300/af98d84f5ee54ab3cafd93c67459acbd.jpg','techno, electronic, minimal, minimal techno, ambient',1),('5827830','Christian Wünsch - Internal Conversion','Christian Wünsch',2014,'Vinyl, 12\", Album','https://api.discogs.com/releases/5827830','Pole Recordings',NULL,108,2140,'https://www.last.fm/music/Christian+W%C3%BCnsch/Internal+Conversion','https://lastfm.freetls.fastly.net/i/u/300x300/d589fca871144520c5cfa63bdcc1b69c.jpg','',1),('5894178','Exium - A Sensible Alternative To Emotion Remixes','Exium',2014,'Vinyl, 12\"','https://api.discogs.com/releases/5894178','Pole Recordings, Eternal Midnight Mastering Studio',NULL,507,9397,'https://www.last.fm/music/Exium/A+Sensible+Alternative+To+Emotion','https://lastfm.freetls.fastly.net/i/u/300x300/301f1d2d55aee986f47a669eb4315ede.jpg','techno, experimental',1),('605307','Doors* - L.A. Woman','The Doors',1971,'Vinyl, LP, Album','https://api.discogs.com/releases/605307','Elektra, Elektra Records, Doors Music Company, Modern Music Publishing Co., Inc., The Doors Workshop, Shorewood Packaging, Columbia Records Pressing Plant, Terre Haute, Artisan Sound Recorders',NULL,1127243,15709011,'https://www.last.fm/music/The+Doors/L.A.+Woman','https://lastfm.freetls.fastly.net/i/u/300x300/2ad5330ea2b590259ca5e8dfb21200d6.jpg','classic rock, psychedelic rock, rock, 60s, blues',1),('612780','Queen - A Night At The Opera','Queen',1975,'Vinyl, LP, Album, Stereo','https://api.discogs.com/releases/612780','EMI, EMI, Queen, EMI Records Ltd., Sarm East Studios, Roundhouse Studios, Olympic Studios, Rockfield Studios, Scorpio Studios, Lansdowne Studios, Sarm East Studios, B. Feldman, Trident Music, Garrod & Lofthouse Ltd., Garrod & Lofthouse Ltd., EMI Records',NULL,745166,10885881,'https://www.last.fm/music/Queen/A+Night+at+the+Opera','https://lastfm.freetls.fastly.net/i/u/300x300/a15e773a42182a7acfe62701d247e297.png','classic rock, rock, hard rock, 1975, 70s',1),('616407','Jeff Mills - The Bells (10th Anniversary)','Jeff Mills',2006,'Vinyl, 12\", 33 ⅓ RPM','https://api.discogs.com/releases/616407','Purpose Maker, Millsart, Mikrofisch-BMG, National Sound Corporation',NULL,394,1648,'https://www.last.fm/music/Jeff+Mills/The+bells','https://lastfm.freetls.fastly.net/i/u/300x300/7ad0e4c463654335bd0c74d59f657b0d.jpg','techno, detroit techno, minimal, electronic, detroit',1),('6886430','Lewis Fautzi - Space Exploration','Lewis Fautzi',2015,'CD, Album','https://api.discogs.com/releases/6886430','Soma Quality Recordings, Soma Recordings Ltd., SPG Publishing UK Ltd, Glowcast Audio Mastering, Soma Recordings Ltd., Soma Recordings Ltd.',NULL,423,3970,'https://www.last.fm/music/Lewis+Fautzi/Space+Exploration','https://lastfm.freetls.fastly.net/i/u/300x300/c1e2afd679ea040b4984729876060336.jpg','techno, electronic, minimal, minimal techno, ambient',1),('6974837','Oscar Mulero - Muscle And Mind','Oscar Mulero',2015,'Vinyl, 12\", Album, Limited Edition','https://api.discogs.com/releases/6974837','Pole Recordings',NULL,1528,23802,'https://www.last.fm/music/Oscar+Mulero/Muscle+and+Mind','https://lastfm.freetls.fastly.net/i/u/300x300/76c2739f6f84f39a590a6e961793e827.jpg','techno, ambient, idm, minimal techno, electronic',1),('7097051','Nirvana - Nevermind','Nirvana',2015,'Vinyl, LP, Album, Reissue, Repress','https://api.discogs.com/releases/7097051','DGC, Sub Pop, Back To Black, Sub Pop Records, The David Geffen Company, The David Geffen Company, Sound City Studios, Scream Studios, Masterdisk, Virgin Songs, Inc., The End Of Music, Universal M & L, Germany',NULL,2639268,50179599,'https://www.last.fm/music/Nirvana/Nevermind','https://lastfm.freetls.fastly.net/i/u/300x300/49cc807f69d59746b6b04be3434e6637.png','grunge, rock, 90s, alternative, alternative rock',1),('7454453','Reeko - Bad Mood EP','Reeko',2015,'Vinyl, 12\", EP','https://api.discogs.com/releases/7454453','Pole Recordings',NULL,NULL,NULL,NULL,NULL,NULL,1),('8162188','David Bowie - The Rise And Fall Of Ziggy Stardust And The Spiders From Mars','David Bowie',2016,'Vinyl, LP, Album, Reissue, Remastered, Repress, Stereo','https://api.discogs.com/releases/8162188','Parlophone, Parlophone, Parlophone, Parlophone, Warner Music Group, GEM, Jones/Tintoretto Entertainment Co., LLC, Jones/Tintoretto Entertainment Co., LLC, Parlophone Records Ltd., Parlophone Records Ltd., Parlophone Records Ltd., Tintoretto Music, RZO Music, Inc., Screen Gems-EMI Music Inc., EMI Music Publishing Ltd., Chrysalis Songs, RZO Music Ltd., Chrysalis Music Ltd., Irving Music, Inc., Rondor Music Ltd., Trident Studios, Air Mastering, Optimal Media GmbH',NULL,425483,11592586,'https://www.last.fm/music/David+Bowie/The+Rise+and+Fall+of+Ziggy+Stardust+and+the+Spiders+From+Mars','https://lastfm.freetls.fastly.net/i/u/300x300/3017b2f31110e4f6de45a212fe93b4a3.png','glam rock, classic rock, 70s, rock, david bowie',1),('9287809','Pink Floyd - The Dark Side Of The Moon','Pink Floyd',2016,'Vinyl, LP, Album, Reissue, Remastered, Stereo','https://api.discogs.com/releases/9287809','Pink Floyd Records, Pink Floyd Records, Pink Floyd Music Ltd., Pink Floyd Music Ltd., Abbey Road Studios, Record Industry, Parlophone Records Ltd., Parlophone Records Ltd., Warner Music Group, Pink Floyd Music Publishers Ltd., Imagem UK Ltd., TRO-Hampshire House Publishing Corp., Roger Waters Music Overseas Ltd., Muziekuitgeverij Artemis B.V., Warner/Chappell Music Publishing Ltd.',NULL,2228677,73838507,'https://www.last.fm/music/Pink+Floyd/The+Dark+Side+of+the+Moon','https://lastfm.freetls.fastly.net/i/u/300x300/d4bdd038cacbec705e269edb0fd38419.png','progressive rock, psychedelic rock, classic rock, rock, pink floyd',1);
/*!40000 ALTER TABLE `albumes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `artistas`
--

DROP TABLE IF EXISTS `artistas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `artistas` (
  `id_artista` varchar(255) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `biografia` text,
  `imagen` varchar(500) DEFAULT NULL,
  `url_discogs` varchar(500) DEFAULT NULL,
  `url_lastfm` varchar(500) DEFAULT NULL,
  `listeners` int DEFAULT '0',
  `plays` int DEFAULT '0',
  `tags` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id_artista`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artistas`
--

LOCK TABLES `artistas` WRITE;
/*!40000 ALTER TABLE `artistas` DISABLE KEYS */;
INSERT INTO `artistas` VALUES ('102727','Reeko','Juan Rico a.k.a. Reeko was born in 1981. In spite of his youth, nowadays this spanish producer born in Asturias is one of the rookie producers with a great future to come in the worldwide techno scene.\r\n\r\nHe has shown his quality skills recording for emerging labels like Music Man Records, Integrale, Pole Recordings, Nheoma, Inceptive,Mechanisms Industries, Theory recordings, Symbolims and Warm Up.\r\n\r\nHe has started to run his own labels, Mental Disorder,Evidence records, mental re-editions and Emphatix records, distributed by triple vision and his online shop, where he is going to continue with his style of dark and effective techno. His live acts are original and heavy in the way of Birmingham sound.\r\n','https://i.discogs.com/pL-wVFJ3bFXL2k3Er_Dbs1wosbTzUm-aqXS7KZzFJNg/rs:fit/g:sm/q:90/h:600/w:400/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9BLTEwMjcy/Ny0xMzU1Njg4NTkx/LTczNDAuanBlZw.jpeg','https://api.discogs.com/artists/102727','https://www.last.fm/music/Reeko',22024,227817,'techno, Industrial Techno, Dark Techno, electronic, t e c h n o'),('1114','Surgeon','English electronic musician and DJ.\r\nMarried to [a3405581].','https://i.discogs.com/_gnYfsqibkxMM-XsVRcnfHOKM4Srmw2QX1s-wY4jB4o/rs:fit/g:sm/q:90/h:400/w:400/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9BLTExMTQt/MTU5MTk2NzEzMi0z/NjAwLmpwZWc.jpeg','https://api.discogs.com/artists/1114','https://www.last.fm/music/Surgeon',94507,1079337,'techno, minimal, electronic, minimal techno, tresor'),('1136','Robert Hood','Robert Hood makes minimal Detroit techno with an emphasis on soul and experimentation over flash and popularity. Having recorded for [l=Metroplex], as well as the Austrian [l=Cheap] label and [a=Jeff Mills]\' [l=Axis] label. Hood started [l=Hardwax] in 1991 (Robert Hood\'s first label prior to forming M-Plant) and also owns and operates the [l=M-Plant] imprint (including the two sublabels Drama and Duet) through which he has released the bulk of his solo material. Hood was a founding member, along with Jeff Mills and Mike Banks, of the [l=Underground Resistance] label, whose influential releases throughout the early and mid-\'90s helped change the face of modern Detroit techno and sparked a creative renaissance. Infusing elements of acid and industrial into a potent blend of Chicago house and Detroit techno, UR\'s aesthetic project and militant business philosophy were (and remain) singular commitments in underground techno. Hood left Detroit (and UR) with Jeff Mills in 1992, setting up shop in New York and recording a series of 12\" EPs. Through the mid-\'90s, Hood has focused on his solo work, setting up M-Plant in 1994 and releasing singles such as \"Internal Empire\", \"Music Data\" and \"Moveable Parts\". Although his desire to remain underground has been replaced by an urge to reach a wider audience, Hood remains fiercely critical of artistic and economic movements destructive to inner-city communities and has combined his musical enterprises with outreach and social activist ends. His debut Peacefrog album \"Point Blank\" took Hood\'s hypnotic minimalism to entirely new depths and territories, whilst his latest album \"Wire To Wire\" takes his productions onto new levels of musicality and sophistication within the world of electronic music.\r\nFather of [a=Lyric Hood].','https://i.discogs.com/phQwnOcG4uBRffZES01L5WfvYvMwQ39vwseW4RYW-1s/rs:fit/g:sm/q:90/h:600/w:457/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9BLTExMzYt/MTI0NDA1MTg2OC5q/cGVn.jpeg','https://api.discogs.com/artists/1136','https://www.last.fm/music/Robert+Hood',134888,1347976,'techno, detroit techno, minimal, detroit, electronic'),('1165','Regis','DJ and producer from UK. He is one of the founders of the labels [l=Downwards], [l=D/N Records], [l=ZET], as well as, the distribution company [l=Integrale Muzique Limited].','https://i.discogs.com/rOReA8Gz68Cx8R5V5a1LdRBpY8L6bU05jGhsptxY-Ew/rs:fit/g:sm/q:90/h:450/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9BLTExNjUt/MTQwODM1MDk2NC0x/MTQxLmpwZWc.jpeg','https://api.discogs.com/artists/1165','https://www.last.fm/music/Regis',35438,644282,'techno, Industrial Techno, electronic, birmingham techno, UK'),('1537114','DVS1','American Techno DJ and music producer based in Minneapolis, US. He is the founder of [l=HUSH (6)] and [l=Mistress Recordings]','https://i.discogs.com/a7zprmSMH9gGoKrD0KFaePgbB9IbwCp7jdGVki6_VXY/rs:fit/g:sm/q:90/h:312/w:472/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9BLTE1Mzcx/MTQtMTUyOTU1Njgw/OC02MTgzLmpwZWc.jpeg','https://api.discogs.com/artists/1537114','https://www.last.fm/music/DVS1',33015,217093,'techno, seen live, electronic, hard techno, minimal techno'),('205','Jeff Mills','DJ, composer, producer and recording artist from Detroit, Michigan, now based in Miami, Florida.\r\nRuns [l=Axis] and its sub-labels.\r\nMarried to [a=Yoko Uozumi].','https://i.discogs.com/RkUGj_cGVM_D6GxvCkZ90K1bs3Rq5zczx0H0UCk5ZMc/rs:fit/g:sm/q:90/h:790/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9BLTIwNS0x/NTA1ODA5NzQ5LTc5/MTAuanBlZw.jpeg','https://api.discogs.com/artists/205','https://www.last.fm/music/Jeff+Mills',162750,2025040,'techno, detroit techno, minimal, electronic, detroit'),('2596','Christian Wünsch','Techno DJ, producer from Spain. Born in Monaco, he spent most of his life in the North of Spain. He started his own labels Tsunami Records and Nine Records.\r\n','https://i.discogs.com/mCHOD7dpDTOdBsG9vy7i0_pb_EebxEWhjYTp1eMA7oU/rs:fit/g:sm/q:90/h:500/w:500/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9BLTI1OTYt/MTYyMjM3NDc3Ni0y/NTYxLmpwZWc.jpeg','https://api.discogs.com/artists/2596','https://www.last.fm/music/+noredirect/Christian+W%C3%BCnsch',1382,14483,'techno, electronic, electronica, Industrial Techno'),('3149532','Lewis Fautzi','','https://i.discogs.com/08fumVY_GISwpvCOS-8ji0NB0usPC6hfaNATsJ03Hs8/rs:fit/g:sm/q:90/h:400/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9BLTMxNDk1/MzItMTM5Mjc1MjM2/OC03Mjg0LmpwZWc.jpeg','https://api.discogs.com/artists/3149532','https://www.last.fm/music/Lewis+Fautzi',17024,114143,'techno, electronic, minimal, minimal techno, electronica'),('5159','Oscar Mulero','Oscar Mulero was born in Madrid, and is a techno DJ and producer. Mulero started DJing in 1988, and was the first Spanish DJ to become part of the Members Of Mayday. He established The Omen Club in Madrid in the early 90s.\r\n\r\nMulero also uses the alias Doctor Smoke for his Drum \'n\' Bass sessions, and owns the labels [l=Warm Up Recordings] and [l=Pole Recordings].\r\n\r\nContact: web@oscarmulero.com\r\n','https://i.discogs.com/d8bXkiC-8AMFtGFbUCr5LaUUjGluMMOW2fVAXQ0xwnw/rs:fit/g:sm/q:90/h:868/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9BLTUxNTkt/MTYwMTU4NTI3Ny01/MTQ1LmpwZWc.jpeg','https://api.discogs.com/artists/5159','https://www.last.fm/music/Oscar+Mulero',37022,350290,'techno, minimal techno, hard techno, electronic, seen live'),('77025','Ben Klock','Ben Klock born in 1972 in the west of Berlin was during the mid-nineties a resident of Cookies in berlin. At the beginning of the 00’s he almost retired from djing because he lost the fun during the Minimal/Micro House wave. In 2005 he was asked to become a Resident for Berghain. Playing there inspired him and revitalized his passion for Techno because of the total freedom what to play there and the extended play time. His style of DJ-ing can be described as Hard but always with a Heart.\r\n\r\nRuns the label [l=Klockworks].','https://i.discogs.com/gZNyxwvwp1cK9aTRPkYJUd79k9XknpHsVOC3CQsrXFU/rs:fit/g:sm/q:90/h:785/w:600/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9BLTc3MDI1/LTE1NDQxMDY5NTAt/OTE0NC5qcGVn.jpeg','https://api.discogs.com/artists/77025','https://www.last.fm/music/Ben+Klock',107933,803258,'techno, minimal, minimal techno, electronic, seen live'),('823','Speedy J','Electronic music producer from Rotterdam, The Netherlands (born 10 August 1969 in Rotterdam).\r\nAfter two albums of electronic listening music on the label Warp, he released two albums with a more experimental sounds in 1997 and 2000. The album Loudboxer (2002) saw a return to a more minimal style of techno.\r\nHe collaborated with Mike Paradinas on the project Slag Boom Van Loon and also released two ambient albums for the FAX +49-69/450464 label under his real name.\r\nIn 2008, Speedy J founded his own record label, Electric Deluxe, releasing his own music as well as records by Terence Fixmer, Gary Beck, Tommy Four Seven and others.','https://i.discogs.com/sKcAUSn41onGazLAHf2ggK-evHsuIshrHUTErje0vR4/rs:fit/g:sm/q:90/h:630/w:533/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9BLTgyMy0x/NTE3NjcwMDAwLTI0/NDMuanBlZw.jpeg','https://api.discogs.com/artists/823','https://www.last.fm/music/Speedy+J',132230,1055998,'techno, electronic, idm, experimental, electronica'),('9566','Exium','Spanish Techno producer and live performer duo.','https://i.discogs.com/Nws3zSFxbvy9J2x76BeMJqNZX5UD8Ftn55O_pin7juA/rs:fit/g:sm/q:90/h:227/w:530/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9BLTk1NjYt/MTI1OTUwNTA3MS5q/cGVn.jpeg','https://api.discogs.com/artists/9566','https://www.last.fm/music/Exium',11555,97380,'techno, Dark Techno, hard techno, birmingham techno, electronic');
/*!40000 ALTER TABLE `artistas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notificaciones`
--

DROP TABLE IF EXISTS `notificaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notificaciones` (
  `id_notificacion` varchar(36) NOT NULL,
  `id_usuario` varchar(36) DEFAULT NULL,
  `id_album` varchar(255) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_notificacion`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_album` (`id_album`),
  CONSTRAINT `notificaciones_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  CONSTRAINT `notificaciones_ibfk_2` FOREIGN KEY (`id_album`) REFERENCES `albumes` (`id_album`) ON DELETE CASCADE,
  CONSTRAINT `notificaciones_chk_1` CHECK ((`estado` in (_utf8mb3'pendiente',_utf8mb3'enviada')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notificaciones`
--

LOCK TABLES `notificaciones` WRITE;
/*!40000 ALTER TABLE `notificaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `notificaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` varchar(36) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES ('5287e312-63dc-44c0-9e4c-6b90c0f1ad12','A','aaaa@gmail.com','scrypt:32768:8:1$YZQ1uGyXRgXIBnl9$25edd2bc0fa949b63f53c2ce7c6649e231261e2ef058a7409d38a22c7db44d855c15684be4adc20aee511bfaf4819d9f133492d5582b05cd742dd919206b0c46','2025-03-19 14:45:47'),('537df240-62e2-4f95-8a50-b7938663d730','ppp','ppp@gmail.com','scrypt:32768:8:1$baKSbaOwe9BXrrLH$ffdf51dedb96efc8d8a225388fe80acb3607f4bef48bb274c89aeb168e009b7829651c01f065998b199af6b4ba2f9f1d726a227451f41a3bf3122305b920b158','2025-03-19 14:46:39'),('c867e79a-26cf-4700-8891-867e5408bc78','Alberto','alberto@gmail.com','scrypt:32768:8:1$GePfgm21K6Z9aIDr$e1dd52a705885388ba401f81b8a910442c44bf95406159320412285295070f7265f761ef6ffbdea19148cc168d59b7f396023a5c9eaa65cdcd4af95ebfd989e7','2025-03-18 10:50:44');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlist`
--

DROP TABLE IF EXISTS `wishlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wishlist` (
  `id_wishlist` varchar(36) NOT NULL,
  `id_usuario` varchar(36) DEFAULT NULL,
  `id_album` varchar(255) DEFAULT NULL,
  `fecha_agregado` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_wishlist`),
  KEY `id_usuario` (`id_usuario`),
  KEY `id_album` (`id_album`),
  CONSTRAINT `wishlist_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  CONSTRAINT `wishlist_ibfk_2` FOREIGN KEY (`id_album`) REFERENCES `albumes` (`id_album`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlist`
--

LOCK TABLES `wishlist` WRITE;
/*!40000 ALTER TABLE `wishlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `wishlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'musicfinder'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-20  8:51:45
