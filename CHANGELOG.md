# Changelog

## [2.0.3] - 2024-10-11

- Remove control object PublishScenarioFile
- Add new control objects SegmentToMO, RotationToMO, ResultsMOToMA
- Remove control object ResultACRM (MOListTransfer)
- Rename control object ResultMODB to MOOffersAgg
- Call logger init only once inside adapters.py

## [2.0.2] - 2024-09-06

- Add new control object SegmentPilotCommRotation

## [2.0.1] - 2024-09-04

- Remove redundant external table in the email templates
- Stop monitor downloading segment from ACRM to MODB (control object = SegmentACRM). It is moved to AirFlow
- Get statistics from all alter score tables and add statistics for theirs union
- Rename control object ScoresStage and templates to ScoreAltScoreLTV 

## [2.0.0] - 2024-07-31

- Switch to python3.12 libraries and new virtual envrironment correspondingly
- Start live on the new test server

## [1.1.4] - 2024-07-05

- Extend statisticts for scores and alter scores at MO
- Add schedule to email template for ltv, scores, alter-scores
- Improve email template for ltv, scores, alter-scores

## [1.1.3] - 2024-05-16

- Fix bug in alter scores statistics calculation
- Add status description in ResultMODB template
- Change schedule - check file trigger every minute (was - 30 seconds)

## [1.1.2] - 2024-04-26

- Add possibility to switch to passive node DB. Make sense for prod (April 24)
- Improve description in templates  (April 24)
- Add new control object - file to trigger MO results transfer to ACRM (April 26)
- Change schedule - now only MO_OFFERS table is checked once pere hour all other objects are checked once per 5 min  (April 24)

## [1.1.1] - 2024-04-19

- Imporve run.sh - when start and pid file exist but there is not proper process - remove pid file and start
- Add oppotunity to set own schedule to each task. Currently only SCENARIO table is checked every 5 minutes
- Correct SQL queries for LTV tables at STAGE and MO
- Implement table selection for alter scores at MODB
- Add link to project description in emails
- Add new  (fields) columns to SCNEARIO emails
- Decided to schedule SCORES, LTV and ACRM to check every 5 min

## [1.1.0] - 2024-03-21

- Major: Extend control objects by addtional step for calculation statistics. Currently used only in ScoresStage
- Move notify_admin from private method to services

## [1.0.3] - 2024-02-14

- Add ScoresStage - new control object for scores
- Improve NoneType error handling in collectors.py

## [1.0.2] - 2023-12-01

- Add ADMIN and USER roles
- Add ADMIN notifiction due to exception
- Improve query for ResultMODB control oject
- More logging druing data collection and check

## [1.0.1] - 2023-11-29

- Improved not working hash fields for CDM.MA_PROCESS_LOAD_STATUS
- Change red color to green in emails

## [1.0.0] - 2023-11-22

- Major changes were done:
- Improve SQL querries for events
- Make EMAIL messages more informative 

## [0.1.2] - 2023-10-30

- Change queries to aCRM use CDM.MA_PROCESS_LOAD_STATUS instead of INTEGRATION.MO_OFFERS.

## [0.1.1] - 2023-10-26

- Improve  Collector class to handle errors during initialization.

## [0.1.0] - 2023-10-24

- Refactor collectors module - separate it onto collectors and control_objects modules.
- Add proper tests.
- Add ugly command line testing mode.

## [0.0.0] - 2023-10-23

:seedling: Initial commit - prerelease.
