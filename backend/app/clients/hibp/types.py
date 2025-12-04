import typing

from pydantic import BaseModel, Field

DataT = typing.TypeVar("DataT")


class HIBPResponse(BaseModel, typing.Generic[DataT]):
    """Generic response wrapper for HIBP API."""

    status: str = Field(default="ok", description="Response status")
    data: typing.Optional[DataT] = Field(None, description="Response data")
    error: typing.Optional[str] = Field(None, description="Error message if any")


class Breach(BaseModel):
    """Represents a single breach from HIBP API."""

    Name: str = Field(
        ...,
        description="A Pascal-cased name representing the breach which is unique across all other breaches. This value never changes and may be used to name dependent assets (such as images) but should not be shown directly to end users (see the 'Title' attribute instead)",
    )
    Title: str = Field(
        ...,
        description="A descriptive title for the breach suitable for displaying to end users. It's unique across all breaches but individual values may change in the future (i.e. if another breach occurs against an organisation already in the system). If a stable value is required to reference the breach, refer to the 'Name' attribute instead",
    )
    Domain: str = Field(
        ...,
        description="The domain of the primary website the breach occurred on. This may be used for identifying other assets external systems may have for the site",
    )
    BreachDate: str = Field(
        ...,
        description="The date (with no time) the breach originally occurred on in ISO 8601 format. This is not always accurate — frequently breaches are discovered and reported long after the original incident. Use this attribute as a guide only",
    )
    AddedDate: str = Field(
        ...,
        description="The date and time (precision to the minute) the breach was added to the system in ISO 8601 format",
    )
    ModifiedDate: str = Field(
        ...,
        description="The date and time (precision to the minute) the breach was modified in ISO 8601 format. This will only differ from the AddedDate attribute if other attributes represented here are changed or data in the breach itself is changed (i.e. additional data is identified and loaded). It is always either equal to or greater then the AddedDate attribute, never less than",
    )
    PwnCount: int = Field(
        ...,
        description="The total number of accounts loaded into the system. This is usually less than the total number reported by the media due to duplication or other data integrity issues in the source data",
    )
    Description: str = Field(
        ...,
        description="Contains an overview of the breach represented in HTML markup. The description may include markup such as emphasis and strong tags as well as hyperlinks",
    )
    LogoPath: str = Field(
        ...,
        description="A URI that specifies where a logo for the breached service can be found. Logos are always in PNG format",
    )
    Attribution: typing.Optional[str] = Field(
        None,
        description="Sometimes requested by the party that provides the data to HIBP",
    )
    DisclosureUrl: typing.Optional[str] = Field(
        None, description="URL to the disclosure or announcement of the breach"
    )
    DataClasses: typing.List[str] = Field(
        ...,
        description="This attribute describes the nature of the data compromised in the breach and contains an alphabetically ordered string array of impacted data classes",
    )
    IsVerified: bool = Field(
        ...,
        description="Indicates that the breach is considered unverified. An unverified breach may not have been hacked from the indicated website. An unverified breach is still loaded into HIBP when there's sufficient confidence that a significant portion of the data is legitimate",
    )
    IsFabricated: bool = Field(
        ...,
        description="Indicates that the breach is considered fabricated. A fabricated breach is unlikely to have been hacked from the indicated website and usually contains a large amount of manufactured data. However, it still contains legitimate email addresses and asserts that the account owners were compromised in the alleged breach",
    )
    IsSensitive: bool = Field(
        ...,
        description="Indicates if the breach is considered sensitive. The public API will not return any accounts for a breach flagged as sensitive",
    )
    IsRetired: bool = Field(
        ...,
        description="Indicates if the breach has been retired. This data has been permanently removed and will not be returned by the API",
    )
    IsSpamList: bool = Field(
        ...,
        description="Indicates if the breach is considered a spam list. This flag has no impact on any other attributes but it means that the data has not come as a result of a security compromise",
    )
    IsMalware: bool = Field(
        ...,
        description="Indicates if the breach is sourced from malware. This flag has no impact on any other attributes, it merely flags that the data was sourced from a malware campaign rather than a security compromise of an online service",
    )
    IsSubscriptionFree: bool = Field(
        ...,
        description="Indicates if the breach is subscription-free. This flag has no impact on any other attributes, it is only used when running a domain search where a sufficiently sized subscription isn't present",
    )
    IsStealerLog: bool = Field(
        ...,
        description="Indicates if the breach is sourced from stealer logs. A breach with this flag also has the domains that appear in the logs loaded against each email address. This data can be accessed via the stealer logs API",
    )


class Paste(BaseModel):
    """Represents a paste from HIBP API."""

    Source: str = Field(
        ...,
        description="The paste service the record was retrieved from. Current values are: Pastebin, Pastie, Slexy, Ghostbin, QuickLeak, JustPaste, AdHocUrl, PermanentOptOut, OptOut",
    )
    Id: str = Field(
        ...,
        description="The ID of the paste as it was given at the source service. Combined with the 'Source' attribute, this can be used to resolve the URL of the paste",
    )
    Title: typing.Optional[str] = Field(
        None,
        description="The title of the paste as observed on the source site. This may be null and if so will be omitted from the response",
    )
    Date: typing.Optional[str] = Field(
        None,
        description="The date and time (precision to the second) that the paste was posted. This is taken directly from the paste site when this information is available but may be null if no date is published",
    )
    EmailCount: int = Field(
        ...,
        description=r"The number of emails that were found when processing the paste. Emails are extracted by using the regular expression \b[a-zA-Z0-9\.\-_\+]+@[a-zA-Z0-9\.\-_]+\.[a-zA-Z]+\b",
    )


class SubscribedDomain(BaseModel):
    """Represents a subscribed domain from HIBP API."""

    DomainName: str = Field(
        ..., description="The full domain name that has been successfully verified"
    )
    PwnCount: typing.Optional[int] = Field(
        None,
        description="The total number of breached email addresses found on the domain at last search (will be null if no searches yet performed)",
    )
    PwnCountExcludingSpamLists: typing.Optional[int] = Field(
        None,
        description="The number of breached email addresses found on the domain at last search, excluding any breaches flagged as a spam list (will be null if no searches yet performed)",
    )
    PwnCountExcludingSpamListsAtLastSubscriptionRenewal: typing.Optional[int] = Field(
        None,
        description="The total number of breached email addresses found on the domain when the current subscription was taken out (will be null if no searches yet performed). This number ensures the domain remains searchable throughout the subscription period even if the volume of breached accounts grows beyond the subscription's scope",
    )
    NextSubscriptionRenewal: typing.Optional[str] = Field(
        None,
        description="The date and time the current subscription ends in ISO 8601 format. The PwnCountExcludingSpamListsAtLastSubscriptionRenewal value is locked in until this time (will be null if there have been no subscriptions)",
    )


class SubscriptionStatus(BaseModel):
    """Represents the subscription status from HIBP API."""

    SubscriptionName: str = Field(
        ...,
        description='The name representing the subscription being either "Pwned 1", "Pwned 2", "Pwned 3" or "Pwned 4"',
    )
    Description: str = Field(
        ...,
        description="A human readable sentence explaining the scope of the subscription",
    )
    SubscribedUntil: str = Field(
        ...,
        description="The date and time the current subscription ends in ISO 8601 format",
    )
    Rpm: int = Field(
        ...,
        description="The rate limit in requests per minute. This applies to the rate the breach search by email address API can be requested",
    )
    DomainSearchMaxBreachedAccounts: int = Field(
        ...,
        description="The size of the largest domain the subscription can search. This is expressed in the total number of breached accounts on the domain, excluding those that appear solely in spam list",
    )
    IncludesStealerLogs: bool = Field(
        ...,
        description="Indicates if the subscription includes access to the stealer logs APIs",
    )
