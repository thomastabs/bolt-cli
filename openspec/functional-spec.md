# Functional Specification

> Per-story Gherkin Acceptance Criteria.
> Appended automatically by bolt after human approval.

## Story 9193405: As a player, I want to see my current points displayed on the scoreboard, so that I know how well I'm performing

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 19:09 UTC

```gherkin
Feature: As a player, I want to see my current points displayed on the scoreboard, so that I know how well I'm performing

  Scenario: Points display updates after catching a fish
    Given the player is in an active game session
    And the scoreboard is displaying the current points total
    When the player catches a fish
    Then the points total on the scoreboard immediately increases by the correct amount for that fish type

  Scenario: Points display shows zero at game start
    Given the player is starting a new game
    When the game initializes
    Then the scoreboard shows 0 points

  Scenario: Points persist during gameplay
    Given the player is in an active game session
    And the player has accumulated points from previous catches
    When the player catches multiple fish
    Then the total points remain accurate and visible throughout the session
```

## Story 9193406: As a player, I want to see the count of fishes I've caught displayed on the scoreboard, so that I can track my fishing success

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 19:09 UTC

```gherkin
Feature: As a player, I want to see the count of fishes I've caught displayed on the scoreboard, so that I can track my fishing success

  Scenario: Fish count increments after successful catch
    Given the player is in an active game session
    And the fish counter on the scoreboard is visible
    When the player successfully catches a fish
    Then the fish counter on the scoreboard increases by one

  Scenario: Fish count starts at zero
    Given the player is beginning a new game
    When the game initializes
    Then the fish count on the scoreboard shows 0

  Scenario: Fish count remains accurate across multiple catches
    Given the player is in an active game session
    When the player catches several fish in succession
    Then the counter accurately reflects the total number of fish caught
```

## Story 9193407: As a player, I want to see the current state of my fishing rod on the scoreboard, so that I know if it's ready to use or needs repair

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 19:09 UTC

```gherkin
Feature: As a player, I want to see the current state of my fishing rod on the scoreboard, so that I know if it's ready to use or needs repair

  Scenario: Rod state shows as ready at game start
    Given the player is starting a new game
    When the game initializes
    Then the rod state indicator on the scoreboard shows the rod is in good condition and ready to fish

  Scenario: Rod state updates when rod takes damage
    Given the player is in an active game session
    And the rod state indicator is displayed on the scoreboard
    When the player's rod takes damage during gameplay
    Then the scoreboard immediately reflects the degraded state of the rod

  Scenario: Rod state shows as broken when durability is depleted
    Given the player is in an active game session
    And the player's rod durability is being tracked
    When the player's rod durability reaches zero
    Then the scoreboard displays that the rod is broken and unusable

  Scenario: Rod state updates after repair
    Given the player is in an active game session
    And the player's rod is broken
    When the player repairs their broken rod
    Then the scoreboard updates to show the rod is functional again
```

## Story 9193408: As a player, I want the scoreboard to be clearly visible during gameplay, so that I can easily monitor my progress without distraction

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 19:09 UTC

```gherkin
Feature: As a player, I want the scoreboard to be clearly visible during gameplay, so that I can easily monitor my progress without distraction

  Scenario: Scoreboard is positioned in a non-intrusive location
    Given the player is in an active game session
    When the scoreboard is rendered on screen
    Then the scoreboard appears in a corner or edge position that does not block the main fishing gameplay area

  Scenario: Scoreboard remains visible during all gameplay states
    Given the player is in an active game session
    When the player is actively fishing, waiting for a catch, or between actions
    Then the scoreboard stays on screen

  Scenario: Scoreboard text is readable
    Given the scoreboard is displayed on a mobile device screen
    When the player views the scoreboard
    Then all text on the scoreboard is large enough and has sufficient contrast to be easily read
```

## Story 9193409: As a player, I want the scoreboard to reset when I start a new game, so that each game session starts fresh

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 19:09 UTC

```gherkin
Feature: As a player, I want the scoreboard to reset when I start a new game, so that each game session starts fresh

  Scenario: All scoreboard values reset to initial state
    Given the player is starting a new game
    When the game initializes
    Then the scoreboard shows 0 points
    And the scoreboard shows 0 fish caught
    And the rod is in ready state

  Scenario: Previous game data does not carry over
    Given the player has completed a game with accumulated points and fish
    When the player starts a new game
    Then the scoreboard does not show any previous session data
```

## Story 9193441: Cast fishing line into the water

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 19:21 UTC

```gherkin
Feature: Cast fishing line into the water

  Scenario: Successful cast
    Given the player is ready to cast
    And the player has sufficient stamina
    When the player taps the cast button
    Then the fishing line extends into the water
    And the bobber appears on the surface
    And the game enters a waiting state for fish to bite

  Scenario: Cast with insufficient stamina
    Given the player has no stamina remaining
    When the player attempts to cast
    Then the cast fails
    And the player receives a message indicating they need to wait for stamina to regenerate

  Scenario: Cast while already fishing
    Given the player has an active line in the water
    When the player attempts to cast
    Then the game prevents the action
    And the game prompts the player to reel in or wait for the current fishing attempt to complete
```

## Story 9193442: Detect when a fish bites the line

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 19:21 UTC

```gherkin
Feature: Detect when a fish bites the line

  Scenario: Fish bite detected
    Given the player has cast their line
    And a fish approaches the line
    When the fish bites the line
    Then the game displays a visual indicator such as bobber movement or animation
    And the game plays an audio cue to alert the player

  Scenario: No fish bite within time limit
    Given the player has cast their line
    And a set duration has passed without a fish biting
    When the time limit expires
    Then the line automatically retracts
    And the fishing attempt ends without catching anything

  Scenario: Multiple fish bites in succession
    Given the player has caught one fish
    And another fish immediately bites
    When the second fish bites the line
    Then the game queues or handles the second bite appropriately
```

## Story 9193443: Reel in the line when a fish bites

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 19:21 UTC

```gherkin
Feature: Reel in the line when a fish bites

  Scenario: Successful reel-in
    Given a fish has bitten the line
    When the player taps the reel button
    Then the line retracts smoothly
    And the fish is pulled toward the player
    And the catch confirmation phase is entered

  Scenario: Reel-in with resistance
    Given a fish has bitten the line
    And the fish is resisting
    When the player continues holding or tapping to reel
    Then the reel speed slows due to resistance
    And the player must overcome the resistance to successfully reel in the fish

  Scenario: Reel-in fails due to line break
    Given a fish has bitten the line
    When the player reels too aggressively or the fish is too strong
    Then the line breaks
    And the fish escapes
    And the fishing attempt ends in failure
```

## Story 9193444: Successfully catch a fish

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 19:21 UTC

```gherkin
Feature: Successfully catch a fish

  Scenario: Fish caught successfully
    Given the player has reeled in a fish
    When the fish is successfully landed
    Then the game displays the fish species, weight, and rewards earned
    And the fish is added to the player's inventory

  Scenario: Catch with bonus multiplier
    Given the player catches a fish during a bonus event or with special equipment
    When the fish is successfully landed
    Then the rewards are multiplied
    And the player receives additional bonus currency or items

  Scenario: Inventory full when catching
    Given the player's inventory is full
    And the player has successfully reeled in a fish
    When the fish is caught
    Then the game prompts the player to discard or sell an item
    And the fish is automatically stored in a temporary holding area
```

## Story 9193445: Fail at catching a fish

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 19:21 UTC

```gherkin
Feature: Fail at catching a fish

  Scenario: Fish escapes during reel-in
    Given the player is reeling in a fish
    When the player fails to reel in the fish quickly enough or with sufficient force
    Then the fish breaks free and escapes
    And the fishing attempt ends
    And the player receives no rewards

  Scenario: Line breaks from excessive force
    Given the player is reeling in a fish
    When the player reels too aggressively or the fish is too strong for the current equipment
    Then the line snaps
    And the fish is lost
    And the player may need to repair or replace their fishing rod

  Scenario: Timeout during reel-in
    Given the player is reeling in a fish
    And a time limit is in effect
    When the player does not reel fast enough within the time limit
    Then the fish loses interest and swims away
    And the fishing attempt ends without a catch
```

## Story 9193446: Cancel fishing attempt

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 19:21 UTC

```gherkin
Feature: Cancel fishing attempt

  Scenario: Cancel before fish bites
    Given the player is waiting for a fish to bite
    When the player taps a cancel or back button
    Then the line retracts immediately
    And the fishing attempt is abandoned without penalty

  Scenario: Cancel during reel-in
    Given the player is actively reeling in a fish
    When the player taps cancel
    Then the reel-in is interrupted
    And the fish escapes
    And the fishing attempt ends

  Scenario: Cancel with confirmation prompt
    Given the player is in an active fishing attempt
    When the player attempts to cancel
    Then a confirmation dialog appears asking if they want to abandon the catch
    And the player confirms the cancellation
    And the attempt is cancelled
```

## Story 9193567: As a player, I want to view a map of fishing lakes, so that I can see available locations to fish

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:28 UTC

```gherkin
Feature: As a player, I want to view a map of fishing lakes, so that I can see available locations to fish

  Scenario: Player opens map and sees all lakes
    Given the player is in the game world
    When the player opens the map screen
    Then a visual representation of the game world is displayed
    And all fishing lakes are marked as distinct icons or locations
    And the map displays with proper zoom level
    And the player can identify each lake

  Scenario: Player views map with no lakes discovered yet
    Given the player is early in the game
    And the player has not discovered any lakes yet
    When the player opens the map
    Then the game world is displayed on the map
    And lakes are hidden or marked as undiscovered
    And the player is prompted to explore

  Scenario: Player navigates map with pan and zoom controls
    Given the player has the map open
    When the player uses touch controls to pan around the map
    And the player zooms in and out to see different areas
    Then the map responds smoothly to pan interactions
    And the map responds smoothly to zoom interactions
    And the map remains readable at different zoom levels
```

## Story 9193568: As a player, I want to see lake details when I select one on the map, so that I can decide which lake to visit

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:28 UTC

```gherkin
Feature: As a player, I want to see lake details when I select one on the map, so that I can decide which lake to visit

  Scenario: Player taps a lake and sees its information
    Given the player has the map open
    And a lake is visible on the map
    When the player taps on a lake icon
    Then a popup or panel appears
    And the lake's name is displayed
    And the fish species available at the lake are shown
    And the difficulty level is displayed
    And any special features are shown
    And the information is clear and easy to read

  Scenario: Player views details for an undiscovered lake
    Given the player has the map open
    And an undiscovered lake is visible on the map
    When the player taps on the undiscovered lake
    Then a details panel appears
    And limited information is displayed
    And some fields are marked as unknown or locked
    And the player is encouraged to visit the lake to learn more

  Scenario: Player closes lake details panel
    Given the lake details panel is open
    When the player taps outside the details panel or presses a close button
    Then the details panel disappears
    And the full map view is displayed
```

## Story 9193569: As a player, I want to navigate to a selected lake from the map, so that I can travel there and start fishing

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:28 UTC

```gherkin
Feature: As a player, I want to navigate to a selected lake from the map, so that I can travel there and start fishing

  Scenario: Player selects a lake and travels to it
    Given the player has the map open
    And a lake is selected
    When the player taps a 'Go' or 'Travel' button
    Then the game transitions to the fishing location at that lake
    And the player is ready to fish

  Scenario: Player attempts to travel to a locked or inaccessible lake
    Given the player has the map open
    And a lake is locked due to story progression or level requirements
    When the player tries to travel to the locked lake
    Then a message is displayed explaining why the lake is inaccessible
    And the message shows what conditions must be met to unlock the lake

  Scenario: Player cancels travel and returns to map
    Given the player has initiated travel to a lake
    When the player cancels the travel action
    Then the game returns to the map view
    And no travel occurs
```

## Story 9193570: As a player, I want to see side quests available on the map, so that I can find additional activities beyond fishing

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:28 UTC

```gherkin
Feature: As a player, I want to see side quests available on the map, so that I can find additional activities beyond fishing

  Scenario: Player views side quest markers on the map
    Given the player opens the map
    When the map is displayed
    Then side quest locations are marked with distinct icons or symbols
    And the side quest icons are visually different from lake icons
    And the side quests are scattered across the map world

  Scenario: Player sees completed and available side quests
    Given the player views the map
    And the player has completed some side quests
    When the map is displayed
    Then completed side quests are shown in a different color or with a checkmark
    And available side quests are visually distinct from completed ones

  Scenario: Player views side quests with no quests available
    Given the player opens the map
    And there are no side quests available in the current area or time
    When the map is displayed
    Then the map displays normally
    And no side quest markers are shown
```

## Story 9193571: As a player, I want to see side quest details when I select one on the map, so that I can understand what the quest involves

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:28 UTC

```gherkin
Feature: As a player, I want to see side quest details when I select one on the map, so that I can understand what the quest involves

  Scenario: Player taps a side quest and sees its details
    Given the player has the map open
    And a side quest marker is visible on the map
    When the player taps on a side quest marker
    Then a panel appears showing the quest name
    And the quest description is displayed
    And the quest objectives are shown
    And the quest rewards are displayed
    And the information helps the player decide if they want to pursue the quest

  Scenario: Player views details for a completed side quest
    Given the player has the map open
    And a completed side quest marker is visible on the map
    When the player taps on the completed side quest
    Then a panel appears showing the quest information
    And the completion status is displayed
    And the rewards they received are shown

  Scenario: Player closes side quest details panel
    Given the side quest details panel is open
    When the player taps outside the details panel or presses a close button
    Then the details panel disappears
    And the map view is displayed
```

## Story 9193572: As a player, I want to navigate to a side quest location from the map, so that I can travel there and complete the quest

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:28 UTC

```gherkin
Feature: As a player, I want to navigate to a side quest location from the map, so that I can travel there and complete the quest

  Scenario: Player selects a side quest and travels to it
    Given the player has the map open
    And a side quest is selected
    When the player taps a 'Go' or 'Travel' button
    Then the game transitions to the quest location
    And the player can begin the quest

  Scenario: Player attempts to travel to a locked or unavailable side quest
    Given the player has the map open
    And a side quest is locked due to level requirements or story progression
    When the player tries to travel to the locked side quest
    Then a message is displayed explaining the requirements to unlock the quest

  Scenario: Player cancels travel to a side quest
    Given the player has initiated travel to a side quest
    When the player cancels the travel action
    Then the game returns to the map view
```

## Story 9193573: As a player, I want to track my progress on the map, so that I can see which lakes I've visited and which quests I've completed

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:28 UTC

```gherkin
Feature: As a player, I want to track my progress on the map, so that I can see which lakes I've visited and which quests I've completed

  Scenario: Player sees visited lakes marked differently on the map
    Given the player has visited some lakes
    And the player opens the map
    When the map is displayed
    Then visited lakes are shown with a different color, icon, or indicator
    And unvisited lakes are visually distinct from visited lakes

  Scenario: Player sees completed quests marked on the map
    Given the player has completed some side quests
    And the player views the map
    When the map is displayed
    Then completed side quests are indicated by a checkmark, different color, or other visual marker

  Scenario: Player views progress statistics on the map
    Given the player opens the map
    When the map screen is displayed
    Then summary statistics are displayed on the map screen
    And the number of lakes visited is shown
    And the number of quests completed is shown
    And the overall exploration percentage is shown
```

## Story 9193574: As a player, I want to filter or toggle map layers, so that I can focus on specific types of locations

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:28 UTC

```gherkin
Feature: As a player, I want to filter or toggle map layers, so that I can focus on specific types of locations

  Scenario: Player toggles lake visibility on the map
    Given the player has the map open
    And map settings or a filter menu is accessible
    When the player toggles the visibility of fishing lakes
    Then when disabled, lake icons disappear from the map
    And when enabled, lake icons reappear on the map

  Scenario: Player toggles side quest visibility on the map
    Given the player has the map open
    And map settings or a filter menu is accessible
    When the player toggles the visibility of side quest markers
    Then when disabled, quest icons disappear from the map
    And when enabled, quest icons reappear on the map

  Scenario: Player uses multiple filters simultaneously
    Given the player has the map open
    And map settings or a filter menu is accessible
    When the player enables or disables multiple map layers at once
    Then the map updates to reflect the selected filters
    And only the enabled layer types are displayed on the map
```

## Story 9193609: View the fishing rod crafting recipe

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:55 UTC

```gherkin
Feature: View the fishing rod crafting recipe

  Scenario: View crafting recipe successfully
    Given the player has access to the crafting menu
    And the fishing rod recipe is unlocked
    When the player opens the crafting menu
    And the player selects the fishing rod option
    Then the game displays the complete recipe
    And all required items are shown with their quantities
    And icons for each required item are displayed

  Scenario: Recipe displays unavailable items
    Given the player has access to the crafting menu
    And the fishing rod recipe is unlocked
    And some required items are not in the player's inventory
    When the player views the fishing rod recipe
    Then required items that are unavailable are highlighted or marked differently
    And the visual distinction indicates items are not in the player's inventory

  Scenario: Recipe not yet unlocked
    Given the player has not met the prerequisite conditions for the fishing rod recipe
    And the player has insufficient level or has not made the required discovery
    When the player tries to view the fishing rod recipe
    Then the recipe is locked or hidden
    And the recipe is not accessible to the player
```

## Story 9193610: Check if all required items are in inventory

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:55 UTC

```gherkin
Feature: Check if all required items are in inventory

  Scenario: All required items are available
    Given the player is on the crafting screen
    And all items required for the fishing rod are in the player's inventory
    And all required items are in sufficient quantities
    When the system checks the inventory status
    Then the system confirms all items are present
    And the 'Craft' button becomes enabled

  Scenario: Some required items are missing
    Given the player is on the crafting screen
    And one or more required items are missing or insufficient in quantity
    When the player checks the inventory status
    Then the system shows which items are missing
    And the system shows which items are insufficient in quantity
    And the 'Craft' button remains disabled
    And a message indicates what is needed

  Scenario: Inventory is full
    Given the player is on the crafting screen
    And all required items are in the player's inventory in sufficient quantities
    And the player's inventory is full
    When the player attempts to craft the fishing rod
    Then the system prevents crafting
    And a message is displayed indicating that inventory space is needed for the crafted rod
```

## Story 9193611: Consume required items from inventory when crafting

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:55 UTC

```gherkin
Feature: Consume required items from inventory when crafting

  Scenario: Items successfully consumed during crafting
    Given the player has initiated crafting
    And all required items are in the player's inventory
    When crafting completes
    Then the required items are deducted from the player's inventory
    And the player's inventory reflects the removal of those items

  Scenario: Crafting is interrupted before completion
    Given the player has started crafting
    And crafting has not yet completed
    When the player closes the game or navigates away
    Then the items remain in the player's inventory
    And no fishing rod is created

  Scenario: Item count drops below requirement mid-craft
    Given the player has initiated crafting with sufficient items
    And crafting is in progress
    When another game event reduces an item count below the requirement before crafting completes
    Then the crafting is cancelled
    And the items are returned to the player's inventory
```

## Story 9193612: Receive the crafted fishing rod in inventory

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:55 UTC

```gherkin
Feature: Receive the crafted fishing rod in inventory

  Scenario: Fishing rod successfully added to inventory
    Given crafting has completed successfully
    And the player's inventory has space available
    When the crafting process finishes
    Then the new fishing rod appears in the player's inventory
    And the fishing rod is immediately available for use in fishing activities

  Scenario: Inventory is full when crafting completes
    Given crafting has completed successfully
    And the player's inventory is full
    When crafting finishes
    Then the system either prompts the player to make space or automatically places the rod in a temporary holding area until space is available

  Scenario: Player receives notification of successful craft
    Given crafting has completed successfully
    When the crafting process finishes
    Then the player sees a confirmation message or animation
    And the message indicates the fishing rod has been successfully crafted
```

## Story 9193613: See a crafting progress indicator

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:55 UTC

```gherkin
Feature: See a crafting progress indicator

  Scenario: Progress bar displays during crafting
    Given the player has initiated crafting
    And crafting is in progress
    When the crafting process begins
    Then a progress bar or timer appears
    And the progress indicator shows the estimated time remaining until the fishing rod is complete

  Scenario: Crafting completes instantly
    Given the player has started crafting
    And the crafting duration is zero or instant
    When the crafting process begins
    Then the progress indicator immediately fills or disappears
    And the indicator shows the rod is ready without delay

  Scenario: Progress indicator persists if player navigates away
    Given the player has started crafting
    And crafting is in progress
    When the player navigates to another screen
    Then the progress continues in the background
    And when the player returns, the progress bar shows the updated status
```

## Story 9193614: Cancel the crafting process

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:55 UTC

```gherkin
Feature: Cancel the crafting process

  Scenario: Cancel crafting before it completes
    Given the player has initiated crafting
    And crafting has not yet completed
    When the player taps the cancel button
    Then the crafting stops
    And all consumed items are returned to the player's inventory

  Scenario: Cannot cancel after crafting is complete
    Given crafting has completed
    And the fishing rod is in the player's inventory
    When the player attempts to cancel
    Then the system does not allow cancellation
    And the fishing rod remains in the player's inventory

  Scenario: Cancel button is unavailable during crafting
    Given the player has initiated crafting
    And crafting is in progress
    When the player tries to cancel
    Then the cancel button is greyed out or disabled
    And the action is prevented during certain crafting stages
```

## Story 9193615: See an error message if crafting fails

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 20:55 UTC

```gherkin
Feature: See an error message if crafting fails

  Scenario: Crafting fails due to missing items
    Given crafting is in progress
    And a required item is no longer available
    When the system detects that a required item is missing during crafting
    Then crafting stops
    And a message explains that an item was lost or used elsewhere

  Scenario: Crafting fails due to game error
    Given crafting is in progress
    When an unexpected system error occurs during crafting
    Then the player receives an error message
    And the items are returned to the player's inventory without penalty

  Scenario: Crafting fails due to insufficient inventory space
    Given crafting has completed
    And the player's inventory is full
    When the system attempts to deliver the crafted rod
    Then the player receives a message explaining the issue
    And the rod is held in a temporary queue
```

## Epic 353350: Out of bait mechanic in Fishing Mobile Video Game

### Story 9193632: As a player, I want to see my current bait count during fishing, so that I know when I'm running low

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:08 UTC

```gherkin
Feature: As a player, I want to see my current bait count during fishing, so that I know when I'm running low

  Scenario: Bait count displayed during active fishing
    Given the player is actively fishing
    When the player casts their line
    Then a bait counter is visible on the screen showing the current number of bait remaining
    And the counter updates in real-time as bait is consumed with each cast

  Scenario: Bait count visible in HUD
    Given the player is in a fishing session
    When the player looks at the heads-up display
    Then the bait count is located in a prominent position on the HUD such as the top corner or bottom bar
    And the bait count is easy to check at a glance

  Scenario: Bait count shows zero
    Given the player has used all their bait
    When the bait count reaches zero
    Then the counter displays zero
    And the counter remains visible on screen
```

### Story 9193633: As a player, I want to receive a warning when my bait is running low, so that I can prepare to restock

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:08 UTC

```gherkin
Feature: As a player, I want to receive a warning when my bait is running low, so that I can prepare to restock

  Scenario: Low bait warning appears
    Given the player is actively fishing
    When the player's bait count drops to 25% or less of their maximum capacity
    Then a visual or audio warning is triggered
    And the player is alerted that bait is running low

  Scenario: Warning is non-intrusive
    Given the player's bait count has dropped to the low threshold
    When the low bait warning is triggered
    Then the warning appears as a subtle notification such as a small icon highlight or gentle sound
    And the warning does not interrupt active gameplay

  Scenario: Warning disappears after restocking
    Given the low bait warning is currently displayed
    When the player restocks bait and the count rises above the low threshold
    Then the warning notification disappears
```

### Story 9193634: As a player, I want to be prevented from casting when I have no bait, so that I don't waste time on impossible actions

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:08 UTC

```gherkin
Feature: As a player, I want to be prevented from casting when I have no bait, so that I don't waste time on impossible actions

  Scenario: Cast button disabled when out of bait
    Given the player's bait count is zero
    When the player looks at the cast button
    Then the cast button is visually disabled grayed out or dimmed
    And the cast button cannot be tapped

  Scenario: Attempted cast with no bait shows error message
    Given the player has no bait remaining
    When the player attempts to cast without bait
    Then a clear error message appears stating 'You are out of bait' or similar
    And the action is prevented

  Scenario: Cast button re-enables after restocking
    Given the cast button is currently disabled due to zero bait
    When the player restocks bait
    Then the cast button immediately becomes active
    And the cast button is tappable again
```

### Story 9193635: As a player, I want to see a clear 'out of bait' screen when I run out, so that I understand what happened and what to do next

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:08 UTC

```gherkin
Feature: As a player, I want to see a clear 'out of bait' screen when I run out, so that I understand what happened and what to do next

  Scenario: Out of bait screen appears automatically
    Given the player has zero bait
    When the player attempts to cast with zero bait or their last bait is consumed
    Then a dedicated screen or modal appears
    And the screen clearly states 'You are out of bait'
    And the bait counter shows zero

  Scenario: Out of bait screen offers restock options
    Given the out of bait screen is displayed
    When the player views the available options
    Then the screen displays buttons or options to restock bait such as 'Buy Bait', 'Use Stored Bait', or 'Return to Menu'
    And the player can choose their next action

  Scenario: Out of bait screen can be dismissed
    Given the out of bait screen is displayed
    When the player taps a close button or back button
    Then the out of bait screen closes
    And the player returns to the fishing area without bait

  Scenario: Out of bait screen appears during a catch attempt
    Given the player is in the middle of a catch sequence
    When the player runs out of bait mid-catch with bait consumed but fish still on line
    Then the catch sequence completes gracefully
    And the out of bait screen appears after the catch sequence completes
    And the out of bait message is shown
```

### Story 9193636: As a player, I want to restock bait from the out of bait screen, so that I can quickly resume fishing

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:08 UTC

```gherkin
Feature: As a player, I want to restock bait from the out of bait screen, so that I can quickly resume fishing

  Scenario: Player purchases bait from out of bait screen
    Given the out of bait screen is displayed
    And the player has sufficient currency
    When the player taps 'Buy Bait'
    And a shop interface appears showing available bait packages
    And the player selects a bait package
    And the player completes the purchase
    Then the bait count updates
    And the purchase is successful

  Scenario: Player uses stored bait from inventory
    Given the out of bait screen is displayed
    And the player has bait stored in their inventory from previous purchases
    When the player taps 'Use Stored Bait'
    Then the bait is transferred to their active fishing supply

  Scenario: Player has no funds or stored bait
    Given the out of bait screen is displayed
    When the player taps 'Buy Bait' but has insufficient currency
    And or the player has no stored bait
    Then a message appears explaining they need more currency
    And the 'Use Stored Bait' option is grayed out or hidden if no stored bait exists

  Scenario: Fishing resumes after restocking
    Given the player has successfully restocked bait
    When the restocking action completes
    Then the out of bait screen closes
    And the player returns to the fishing area
    And the bait count is updated
    And the cast button is re-enabled
```

### Story 9193637: As a player, I want bait to be consumed only when I successfully cast, so that I'm not penalized for failed attempts

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:08 UTC

```gherkin
Feature: As a player, I want bait to be consumed only when I successfully cast, so that I'm not penalized for failed attempts

  Scenario: Bait consumed on successful cast
    Given the player has bait available
    When the player taps the cast button
    And the line is successfully thrown into the water
    Then the bait count decreases by one

  Scenario: Bait not consumed on cancelled cast
    Given the player has initiated a cast
    When the player cancels the cast before the line is fully deployed
    Then the bait count remains unchanged

  Scenario: Bait not consumed on failed cast
    Given the player has initiated a cast
    When a cast fails due to a game error or technical issue
    Then the bait is not deducted from the player's count
```

### Story 9193638: As a player, I want to see how much bait I have in my inventory, so that I can plan my fishing sessions

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:08 UTC

```gherkin
Feature: As a player, I want to see how much bait I have in my inventory, so that I can plan my fishing sessions

  Scenario: Inventory screen shows total bait
    Given the player is in the game
    When the player opens their inventory or profile screen
    Then the total amount of bait they have stored is visible
    And the stored bait is shown separately from their active fishing bait

  Scenario: Inventory distinguishes active vs stored bait
    Given the inventory screen is open
    When the player views the bait information
    Then the inventory clearly shows how much bait is currently active in use
    And the inventory clearly shows how much bait is stored in reserve
    And the player can understand their total resources

  Scenario: Inventory updates after restocking
    Given the player has restocked bait during a fishing session
    When the player opens the inventory screen
    Then the inventory screen reflects the updated bait count
```

## Epic 353351: Create health bar in Fishing Mobile Video Game

### Story 9193662: Health Bar Display At Game Start

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:20 UTC

```gherkin
Feature: Health Bar Display At Game Start

  Scenario: Health bar displays at game start
    Given the player has not yet started a new fishing game
    When the player starts a new fishing game
    Then the health bar appears on the screen
    And the health bar shows full health
    And the health bar is clearly visible
    And the health bar is positioned in a convenient location like the top-left or top-right corner

  Scenario: Health bar shows correct initial value
    Given the player has just started a new game
    When the health bar is rendered
    Then the health bar displays the player's starting health value of 100 HP
    And the visual representation fills the entire bar width
    And the bar indicates maximum health

  Scenario: Health bar is not visible before game starts
    Given the player has not entered gameplay
    When the game is in the pre-game state
    Then the health bar is hidden
    And the health bar is not rendered
    And the health bar only appears once the game session begins
```

### Story 9193663: Health Bar Decreases On Damage

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:20 UTC

```gherkin
Feature: Health Bar Decreases On Damage

  Scenario: Health bar decreases on damage
    Given the player has full health of 100 HP
    And the player is in active gameplay
    When the player takes 25 damage from an enemy or hazard
    Then the health bar visually shrinks proportionally
    And the health bar fills approximately 75% of its width

  Scenario: Health bar updates immediately
    Given the player is in active gameplay
    And the player has taken damage
    When a damage event occurs
    Then the health bar responds instantly to the damage event
    And there is no delay or lag in the visual update
    And the player receives immediate visual feedback

  Scenario: Health bar handles multiple damage hits
    Given the player is in active gameplay
    And the player has full health
    When the player takes multiple consecutive hits
    Then the health bar decreases smoothly with each hit
    And the bar continues to shrink accurately with each damage event

  Scenario: Health bar does not go below zero
    Given the player has 10 HP remaining
    And the player is in active gameplay
    When the player takes damage that would reduce health below zero
    Then the health bar stops at zero
    And the health bar does not display negative values
    And the health bar does not extend beyond the left edge
```

### Story 9193664: Health Bar Increases On Healing

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:20 UTC

```gherkin
Feature: Health Bar Increases On Healing

  Scenario: Health bar increases when healing item is used
    Given the player has 50 HP
    And the player has a healing potion in inventory
    And the healing potion restores 30 HP
    When the player uses the healing potion
    Then the health bar visually expands
    And the health bar fills to 80% width

  Scenario: Health bar does not exceed maximum
    Given the player has a healing item in inventory
    When the player uses a healing item when already at full health
    And or the player uses a healing item that would exceed maximum health
    Then the bar stays at full width
    And the health bar does not overflow

  Scenario: Health bar updates when no healing items available
    Given the player has no healing items in inventory
    When the player attempts to use a healing item
    Then the health bar remains unchanged
    And the player receives feedback that no items are available
```

### Story 9193665: Health Bar Color Changes At Thresholds

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:20 UTC

```gherkin
Feature: Health Bar Color Changes At Thresholds

  Scenario: Health bar is green at high health
    Given the player is in active gameplay
    When the player has more than 50% health remaining
    Then the health bar displays in green color
    And the green color indicates a safe status

  Scenario: Health bar turns yellow at medium health
    Given the player is in active gameplay
    When the player's health drops to between 25% and 50%
    Then the health bar changes to yellow
    And the yellow color warns the player they are taking damage

  Scenario: Health bar turns red at critical health
    Given the player is in active gameplay
    When the player's health drops below 25%
    Then the health bar turns red
    And the red color indicates critical danger
    And the red color indicates imminent defeat

  Scenario: Color transitions smoothly
    Given the player is in active gameplay
    And the player has high health
    When the player takes damage and health decreases
    Then the color transitions gradually from green to yellow to red
    And there are no jarring visual jumps
```

### Story 9193666: Health Bar Displays Numeric Value

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:20 UTC

```gherkin
Feature: Health Bar Displays Numeric Value

  Scenario: Numeric health value displays next to bar
    Given the player is in active gameplay
    And the player has 75 HP out of 100 maximum
    When the health bar is rendered
    Then the health bar shows a text label displaying the current health and maximum health
    And the text displays as '75/100'
    And the text is readable
    And the text is positioned clearly near the bar

  Scenario: Numeric value updates with damage and healing
    Given the player is in active gameplay
    And the numeric health display is visible
    When the player takes damage or uses healing items
    Then the numeric display updates immediately
    And the numeric display reflects the new health value

  Scenario: Numeric value displays zero when health depleted
    Given the player is in active gameplay
    When the player's health reaches zero
    Then the numeric display shows '0/100' or similar
    And the numeric display confirms the player is defeated
```

### Story 9193667: Health Bar Disappears On Player Death

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:20 UTC

```gherkin
Feature: Health Bar Disappears On Player Death

  Scenario: Health bar hides on player death
    Given the player is in active gameplay
    And the player's health is at zero
    When the player is defeated
    And the game transitions to a game-over screen
    Then the health bar fades out
    And the health bar disappears from the screen

  Scenario: Health bar remains visible until death is confirmed
    Given the player is in active gameplay
    When the player has 1 HP remaining
    Then the health bar stays on screen
    And the health bar remains visible while the player is alive
    And the health bar only disappears after the death animation or game-over sequence begins

  Scenario: Health bar reappears on game restart
    Given the player has completed a game session
    And the player is restarting the game or loading a new session
    When the new game begins
    Then the health bar reappears
    And the health bar displays with full health
    And the health bar is ready for the next game
```

## Epic 353352: Create crouch mechanic for Fishing Mobile Video Game

### Story 9193685: Player Enters Crouch Mode

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:33 UTC

```gherkin
Feature: Player Enters Crouch Mode

  Scenario: Player successfully enters crouch mode
    Given the player is standing in normal stance
    When the player taps the crouch button on the screen
    Then the player character transitions to a crouched stance
    And the character model visibly lowers
    And the crouch button remains highlighted to indicate active crouch mode

  Scenario: Player exits crouch mode by pressing button again
    Given the player is in crouch mode
    When the player taps the crouch button again
    Then the character stands back up to normal height
    And the crouch button returns to its inactive state

  Scenario: Crouch button is unresponsive during animation
    Given the character is mid-animation (e.g., casting a line)
    When the player taps the crouch button
    Then the button press is ignored
    And the character continues the current animation without interruption
```

### Story 9193686: Movement Speed Decreases When Crouching

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:33 UTC

```gherkin
Feature: Movement Speed Decreases When Crouching

  Scenario: Player moves slower while crouched
    Given the player is in crouch mode
    When the player moves forward using the movement controls
    Then the character moves noticeably slower than normal walking speed
    And the movement appears deliberate and stealthy

  Scenario: Speed returns to normal when exiting crouch
    Given the player is moving while in crouch mode
    When the player exits crouch mode
    Then the character immediately accelerates back to normal movement speed

  Scenario: Player cannot move at all if crouch speed is zero
    Given the game is configured with zero crouch speed
    And the player is in crouch mode
    When the player attempts to move
    Then the character remains stationary
    And the character does not respond to movement input
```

### Story 9193687: Camera Adjusts When Crouching

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:33 UTC

```gherkin
Feature: Camera Adjusts When Crouching

  Scenario: Camera lowers when entering crouch mode
    Given the player is standing with the camera at normal height
    When the player enters crouch mode
    Then the camera smoothly lowers to match the crouched character height
    And the player sees the fishing area from a lower vantage point

  Scenario: Camera returns to normal height when exiting crouch
    Given the player is in crouch mode with the camera lowered
    When the player exits crouch mode
    Then the camera smoothly rises back to the normal standing camera height

  Scenario: Camera adjustment is blocked by obstacles
    Given the player is in a tight space where the lowered camera would clip through terrain or objects
    When the player enters crouch mode
    Then the camera adjusts to the maximum safe distance without clipping
    And the player receives the best available view
```

### Story 9193688: Crouch Mode Reduces Visibility To Fish

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:33 UTC

```gherkin
Feature: Crouch Mode Reduces Visibility To Fish

  Scenario: Fish remain calm when player crouches nearby
    Given the player approaches a fish while standing
    And the fish begins to flee
    When the player enters crouch mode and moves closer
    Then the fish stops fleeing
    And the fish returns to normal behavior
    And the player can get within casting range

  Scenario: Fish still flee if player moves too close while crouching
    Given the player is crouched and approaching a fish very slowly
    When the player gets too close (within a minimum distance)
    Then the fish still flees despite the crouch
    And the player has violated the fish's personal space

  Scenario: Fish react normally when player stands up
    Given the player is crouched near a calm fish
    When the player stands up
    Then the fish immediately detects the movement
    And the fish begins to flee
```

### Story 9193689: Visual Feedback Shows Crouch State

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:33 UTC

```gherkin
Feature: Visual Feedback Shows Crouch State

  Scenario: Character model visibly crouches
    Given the player is standing in normal stance
    When the player enters crouch mode
    Then the character model transitions to a crouched pose with bent knees and lowered torso

  Scenario: UI indicator shows crouch status
    Given the player is standing
    When the player enters crouch mode
    Then a crouch status indicator (icon or text) appears on the HUD

  Scenario: UI indicator disappears when exiting crouch
    Given the player is in crouch mode with the status indicator visible
    When the player exits crouch mode
    Then the crouch status indicator disappears from the HUD

  Scenario: No visual feedback if crouch is disabled
    Given crouch is disabled in the current game area or due to game state
    When the player presses the crouch button
    Then nothing happens visually
    And nothing happens mechanically
```

### Story 9193690: Cannot Crouch During Certain Actions

**Status:** Gherkin Locked  
**Locked at:** 2026-04-24 21:33 UTC

```gherkin
Feature: Cannot Crouch During Certain Actions

  Scenario: Player cannot crouch while casting a fishing line
    Given the player is in the middle of a casting animation
    When the player attempts to press the crouch button
    Then the input is ignored
    And the character remains standing until the cast completes

  Scenario: Player cannot crouch while reeling in a fish
    Given the player is actively reeling in a caught fish
    When the player presses the crouch button
    Then the crouch button is disabled
    And pressing it has no effect

  Scenario: Player can crouch again after action completes
    Given the player has finished casting or reeling
    When the player presses the crouch button
    Then the crouch button becomes active
    And the player can immediately enter crouch mode
```
