Feature: Limit the number of changesets per push
    In order to make backouts easier
    As a Mercurial user
    I would like to limit the number of changesets per push

    Background:
        Given a web-served repository
        And the changeset limiting hook
        And a local clone

    Scenario: A push with more changesets than allowed is rejected
        When I set the changesets per push limit to 2
        And I try to push 3 changesets to the web-served repository
        Then my changesets are not accepted

    Scenario: A push with exactly the changeset limit is accepted
        When I set the changesets per push limit to 3
        And I try to push 3 changesets to the web-served repository
        Then my changesets are accepted

    Scenario: A push with less than the changeset limit is accepted
        When I set the changesets per push limit to 4
        And I try to push 3 changesets to the web-served repository
        Then my changesets are accepted

    Scenario: The limit can be disabled without removing the hook
        When I set the changesets per push limit to 0
        And I try to push 4 changesets to the web-served repository
        Then my changesets are accepted

    Scenario: The limit only applies to the default branch
        When I set the changesets per push limit to 1
        And I try to push 2 changesets to a named branch
        Then my changesets are accepted
