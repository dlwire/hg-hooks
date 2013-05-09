Feature: Only the person holding the baton should be able to push to the default branch

    Background:
        Given a web-served repository
        And the baton hook
        And a local clone

    Scenario: When I have the BATON comment I can push
        When I push with the comment 'BATON'
        Then my changesets are accepted

    Scenario: When I don't have the BATON comment I can't push
        When I push without the comment 'BATON'
        Then my changesets are not accepted

    Scenario: When I don't have the BATON comment I push to a different branch
        When I push without the comment 'BATON' to a named branch
        Then my changesets are accepted
