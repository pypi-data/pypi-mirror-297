from __future__ import annotations

from decimal import Decimal
from enum import Enum
from functools import lru_cache, singledispatchmethod

from pydantic import Field

from pycountries._base import EnumTypeBase, UnitBase


class CurrencyUnit(UnitBase):
    alpha_3: str = Field(
        min_length=3,
        max_length=3,
        description="A three-letter alphabetic code. "
        "This alphabetic code is used internationally to represent currency in financial "
        "transaction and data. "
        "It is standardized by the International Organization for Standardization (ISO) to facilitate "
        "consistency and clarity in financial communications.",
        examples=[
            "USD",
            "EUR",
            "RUB",
        ],
    )
    numeric: str = Field(
        min_length=3,
        max_length=3,
        description="Numeric code. Used to represent currency in context where numerical representation "
        "is preferred over alphabetic ones, such as in databases or systems where numeric identifier "
        "is easier to work with.",
        examples=[
            "840",
            "978",
            "643",
        ],
    )
    digits: int = Field(
        default=2,
        description="The maximum number of decimal places that are typically used when dealing with a currency.",
        examples=[
            "2",
            "2",
            "2",
        ],
    )
    name: str = Field(
        description="Official title of a currency",
        examples=[
            "US Dollar",
            "Euro",
            "Russian Ruble",
        ],
    )


@lru_cache(maxsize=3)
def _get_currencies_by_digits(
    digits: int,
    /,
) -> list[Currency]:
    currency_list = []
    _members = Currency.__members__.values()
    currency: Currency
    for currency in _members:
        if currency.digits == digits:
            currency_list.append(currency)
    return currency_list


class _CurrencyEnumType(EnumTypeBase):
    def __call__(cls, value, *args, **kw):  # noqa: N805
        _members = cls.__members__.values()  # type: ignore[var-annotated]
        currency: Currency
        for currency in _members:
            if value in [
                currency.alpha_3,
                currency.numeric,
                int(currency.numeric),
            ]:
                return currency
        raise ValueError(f'"{value}" is not a valid {cls.__qualname__}') from None

    @property
    def zero_digits(cls) -> list[Currency]:  # noqa: N805
        """
        Returns:
            ISO 4217 currencies with no digits (decimals).
        """
        return _get_currencies_by_digits(0)

    @property
    def two_digits(cls) -> list[Currency]:  # noqa: N805
        """
        Returns:
            ISO 4217 currencies with two digits (decimals).
        """
        return _get_currencies_by_digits(2)

    @property
    def three_digits(cls) -> list[Currency]:  # noqa: N805
        """
        Returns:
            ISO 4217 currencies with three digits (decimals).
        """
        return _get_currencies_by_digits(3)


class BaseCurrencyError(Exception):
    """Base Currency Error."""


class WrongAmountTypeError(BaseCurrencyError):
    """Wrong Amount Type Error"""


class NegativeAmountNotAllowedError(BaseCurrencyError):
    """Negative Amount Not Allowed Error"""


class ZeroAmountNotAllowedError(BaseCurrencyError):
    """Zero Amount Not Allowed Error"""


class AmountSpecialValuesNotAllowedError(BaseCurrencyError):
    """Amount Special Values Not Allowed Error."""


class WrongAmountDigitsNumberError(BaseCurrencyError):
    """Wrong Amount Digits Number Error."""


class Currency(Enum, metaclass=_CurrencyEnumType):
    """
    The Currency Enum is a comprehensive collection designed to facilitate currency handling in software applications.
    It encompasses the ISO 4217 standard, which defines alphabetic and numeric codes for currencies,
    along with their corresponding full names.

    This Enum provides developers with a structured and standardized way to represent and manage currencies.
    Whether for financial transactions, currency conversion, or reporting purposes,
    the Currency Enum offers a reliable reference for accurately identifying and working with currencies across
    diverse software environments.
    """

    AED = CurrencyUnit(
        alpha_3="AED",
        numeric="784",
        name="UAE Dirham",
    )
    AFN = CurrencyUnit(
        alpha_3="AFN",
        numeric="971",
        name="Afghani",
    )
    ALL = CurrencyUnit(
        alpha_3="ALL",
        numeric="008",
        name="Lek",
    )
    AMD = CurrencyUnit(
        alpha_3="AMD",
        numeric="051",
        name="Armenian Dram",
    )
    ANG = CurrencyUnit(
        alpha_3="ANG",
        numeric="532",
        name="Netherlands Antillean Guilder",
    )
    AOA = CurrencyUnit(
        alpha_3="AOA",
        numeric="973",
        name="Kwanza",
    )
    ARS = CurrencyUnit(
        alpha_3="ARS",
        numeric="032",
        name="Argentine Peso",
    )
    AUD = CurrencyUnit(
        alpha_3="AUD",
        numeric="036",
        name="Australian Dollar",
    )
    AWG = CurrencyUnit(
        alpha_3="AWG",
        numeric="533",
        name="Aruban Florin",
    )
    AZN = CurrencyUnit(
        alpha_3="AZN",
        numeric="944",
        name="Azerbaijan Manat",
    )
    BAM = CurrencyUnit(
        alpha_3="BAM",
        numeric="977",
        name="Convertible Mark",
    )
    BBD = CurrencyUnit(
        alpha_3="BBD",
        numeric="052",
        name="Barbados Dollar",
    )
    BDT = CurrencyUnit(
        alpha_3="BDT",
        numeric="050",
        name="Taka",
    )
    BGN = CurrencyUnit(
        alpha_3="BGN",
        numeric="975",
        name="Bulgarian Lev",
    )
    BHD = CurrencyUnit(
        alpha_3="BHD",
        numeric="048",
        name="Bahraini Dinar",
        digits=3,
    )
    BIF = CurrencyUnit(
        alpha_3="BIF",
        numeric="108",
        name="Burundi Franc",
        digits=0,
    )
    BMD = CurrencyUnit(
        alpha_3="BMD",
        numeric="060",
        name="Bermudian Dollar",
    )
    BND = CurrencyUnit(
        alpha_3="BND",
        numeric="096",
        name="Brunei Dollar",
    )
    BOB = CurrencyUnit(
        alpha_3="BOB",
        numeric="068",
        name="Boliviano",
    )
    BOV = CurrencyUnit(
        alpha_3="BOV",
        numeric="984",
        name="Mvdol",
    )
    BRL = CurrencyUnit(
        alpha_3="BRL",
        numeric="986",
        name="Brazilian Real",
    )
    BSD = CurrencyUnit(
        alpha_3="BSD",
        numeric="044",
        name="Bahamian Dollar",
    )
    BTN = CurrencyUnit(
        alpha_3="BTN",
        numeric="064",
        name="Ngultrum",
    )
    BWP = CurrencyUnit(
        alpha_3="BWP",
        numeric="072",
        name="Pula",
    )
    BYN = CurrencyUnit(
        alpha_3="BYN",
        numeric="933",
        name="Belarusian Ruble",
    )
    BZD = CurrencyUnit(
        alpha_3="BZD",
        numeric="084",
        name="Belize Dollar",
    )
    CAD = CurrencyUnit(
        alpha_3="CAD",
        numeric="124",
        name="Canadian Dollar",
    )
    CDF = CurrencyUnit(
        alpha_3="CDF",
        numeric="976",
        name="Congolese Franc",
    )
    CHE = CurrencyUnit(
        alpha_3="CHE",
        numeric="947",
        name="WIR Euro",
    )
    CHF = CurrencyUnit(
        alpha_3="CHF",
        numeric="756",
        name="Swiss Franc",
    )
    CHW = CurrencyUnit(
        alpha_3="CHW",
        numeric="948",
        name="WIR Franc",
    )
    CLF = CurrencyUnit(
        alpha_3="CLF",
        numeric="990",
        name="Unidad de Fomento",
    )
    CLP = CurrencyUnit(
        alpha_3="CLP",
        numeric="152",
        name="Chilean Peso",
        digits=0,
    )
    CNY = CurrencyUnit(
        alpha_3="CNY",
        numeric="156",
        name="Yuan Renminbi",
    )
    COP = CurrencyUnit(
        alpha_3="COP",
        numeric="170",
        name="Colombian Peso",
    )
    COU = CurrencyUnit(
        alpha_3="COU",
        numeric="970",
        name="Unidad de Valor Real",
    )
    CRC = CurrencyUnit(
        alpha_3="CRC",
        numeric="188",
        name="Costa Rican Colon",
    )
    CUC = CurrencyUnit(
        alpha_3="CUC",
        numeric="931",
        name="Peso Convertible",
    )
    CUP = CurrencyUnit(
        alpha_3="CUP",
        numeric="192",
        name="Cuban Peso",
    )
    CVE = CurrencyUnit(
        alpha_3="CVE",
        numeric="132",
        name="Cabo Verde Escudo",
    )
    CZK = CurrencyUnit(
        alpha_3="CZK",
        numeric="203",
        name="Czech Koruna",
    )
    DJF = CurrencyUnit(
        alpha_3="DJF",
        numeric="262",
        name="Djibouti Franc",
        digits=0,
    )
    DKK = CurrencyUnit(
        alpha_3="DKK",
        numeric="208",
        name="Danish Krone",
    )
    DOP = CurrencyUnit(
        alpha_3="DOP",
        numeric="214",
        name="Dominican Peso",
    )
    DZD = CurrencyUnit(
        alpha_3="DZD",
        numeric="012",
        name="Algerian Dinar",
    )
    EGP = CurrencyUnit(
        alpha_3="EGP",
        numeric="818",
        name="Egyptian Pound",
    )
    ERN = CurrencyUnit(
        alpha_3="ERN",
        numeric="232",
        name="Nakfa",
    )
    ETB = CurrencyUnit(
        alpha_3="ETB",
        numeric="230",
        name="Ethiopian Birr",
    )
    EUR = CurrencyUnit(
        alpha_3="EUR",
        numeric="978",
        name="Euro",
    )
    FJD = CurrencyUnit(
        alpha_3="FJD",
        numeric="242",
        name="Fiji Dollar",
    )
    FKP = CurrencyUnit(
        alpha_3="FKP",
        numeric="238",
        name="Falkland Islands Pound",
    )
    GBP = CurrencyUnit(
        alpha_3="GBP",
        numeric="826",
        name="Pound Sterling",
    )
    GEL = CurrencyUnit(
        alpha_3="GEL",
        numeric="981",
        name="Lari",
    )
    GHS = CurrencyUnit(
        alpha_3="GHS",
        numeric="936",
        name="Ghana Cedi",
    )
    GIP = CurrencyUnit(
        alpha_3="GIP",
        numeric="292",
        name="Gibraltar Pound",
    )
    GMD = CurrencyUnit(
        alpha_3="GMD",
        numeric="270",
        name="Dalasi",
    )
    GNF = CurrencyUnit(
        alpha_3="GNF",
        numeric="324",
        name="Guinean Franc",
        digits=0,
    )
    GTQ = CurrencyUnit(
        alpha_3="GTQ",
        numeric="320",
        name="Quetzal",
    )
    GYD = CurrencyUnit(
        alpha_3="GYD",
        numeric="328",
        name="Guyana Dollar",
    )
    HKD = CurrencyUnit(
        alpha_3="HKD",
        numeric="344",
        name="Hong Kong Dollar",
    )
    HNL = CurrencyUnit(
        alpha_3="HNL",
        numeric="340",
        name="Lempira",
    )
    HRK = CurrencyUnit(
        alpha_3="HRK",
        numeric="191",
        name="Kuna",
    )
    HTG = CurrencyUnit(
        alpha_3="HTG",
        numeric="332",
        name="Gourde",
    )
    HUF = CurrencyUnit(
        alpha_3="HUF",
        numeric="348",
        name="Forint",
    )
    IDR = CurrencyUnit(
        alpha_3="IDR",
        numeric="360",
        name="Rupiah",
    )
    ILS = CurrencyUnit(
        alpha_3="ILS",
        numeric="376",
        name="New Israeli Sheqel",
    )
    INR = CurrencyUnit(
        alpha_3="INR",
        numeric="356",
        name="Indian Rupee",
    )
    IQD = CurrencyUnit(
        alpha_3="IQD",
        numeric="368",
        name="Iraqi Dinar",
    )
    IRR = CurrencyUnit(
        alpha_3="IRR",
        numeric="364",
        name="Iranian Rial",
    )
    ISK = CurrencyUnit(
        alpha_3="ISK",
        numeric="352",
        name="Iceland Krona",
    )
    JMD = CurrencyUnit(
        alpha_3="JMD",
        numeric="388",
        name="Jamaican Dollar",
    )
    JOD = CurrencyUnit(
        alpha_3="JOD",
        numeric="400",
        name="Jordanian Dinar",
        digits=3,
    )
    JPY = CurrencyUnit(
        alpha_3="JPY",
        numeric="392",
        name="Yen",
        digits=0,
    )
    KES = CurrencyUnit(
        alpha_3="KES",
        numeric="404",
        name="Kenyan Shilling",
    )
    KGS = CurrencyUnit(
        alpha_3="KGS",
        numeric="417",
        name="Som",
    )
    KHR = CurrencyUnit(
        alpha_3="KHR",
        numeric="116",
        name="Riel",
    )
    KMF = CurrencyUnit(
        alpha_3="KMF",
        numeric="174",
        name="Comorian Franc",
        digits=0,
    )
    KPW = CurrencyUnit(
        alpha_3="KPW",
        numeric="408",
        name="North Korean Won",
    )
    KRW = CurrencyUnit(
        alpha_3="KRW",
        numeric="410",
        name="Won",
        digits=0,
    )
    KWD = CurrencyUnit(
        alpha_3="KWD",
        numeric="414",
        name="Kuwaiti Dinar",
        digits=3,
    )
    KYD = CurrencyUnit(
        alpha_3="KYD",
        numeric="136",
        name="Cayman Islands Dollar",
    )
    KZT = CurrencyUnit(
        alpha_3="KZT",
        numeric="398",
        name="Tenge",
    )
    LAK = CurrencyUnit(
        alpha_3="LAK",
        numeric="418",
        name="Lao Kip",
    )
    LBP = CurrencyUnit(
        alpha_3="LBP",
        numeric="422",
        name="Lebanese Pound",
    )
    LKR = CurrencyUnit(
        alpha_3="LKR",
        numeric="144",
        name="Sri Lanka Rupee",
    )
    LRD = CurrencyUnit(
        alpha_3="LRD",
        numeric="430",
        name="Liberian Dollar",
    )
    LSL = CurrencyUnit(
        alpha_3="LSL",
        numeric="426",
        name="Loti",
    )
    LYD = CurrencyUnit(
        alpha_3="LYD",
        numeric="434",
        name="Libyan Dinar",
    )
    MAD = CurrencyUnit(
        alpha_3="MAD",
        numeric="504",
        name="Moroccan Dirham",
    )
    MDL = CurrencyUnit(
        alpha_3="MDL",
        numeric="498",
        name="Moldovan Leu",
    )
    MGA = CurrencyUnit(
        alpha_3="MGA",
        numeric="969",
        name="Malagasy Ariary",
        digits=0,
    )
    MKD = CurrencyUnit(
        alpha_3="MKD",
        numeric="807",
        name="Denar",
    )
    MMK = CurrencyUnit(
        alpha_3="MMK",
        numeric="104",
        name="Kyat",
    )
    MNT = CurrencyUnit(
        alpha_3="MNT",
        numeric="496",
        name="Tugrik",
    )
    MOP = CurrencyUnit(
        alpha_3="MOP",
        numeric="446",
        name="Pataca",
    )
    MRU = CurrencyUnit(
        alpha_3="MRU",
        numeric="929",
        name="Ouguiya",
    )
    MUR = CurrencyUnit(
        alpha_3="MUR",
        numeric="480",
        name="Mauritius Rupee",
    )
    MVR = CurrencyUnit(
        alpha_3="MVR",
        numeric="462",
        name="Rufiyaa",
    )
    MWK = CurrencyUnit(
        alpha_3="MWK",
        numeric="454",
        name="Malawi Kwacha",
    )
    MXN = CurrencyUnit(
        alpha_3="MXN",
        numeric="484",
        name="Mexican Peso",
    )
    MXV = CurrencyUnit(
        alpha_3="MXV",
        numeric="979",
        name="Mexican Unidad de Inversion (UDI)",
    )
    MYR = CurrencyUnit(
        alpha_3="MYR",
        numeric="458",
        name="Malaysian Ringgit",
    )
    MZN = CurrencyUnit(
        alpha_3="MZN",
        numeric="943",
        name="Mozambique Metical",
    )
    NAD = CurrencyUnit(
        alpha_3="NAD",
        numeric="516",
        name="Namibia Dollar",
    )
    NGN = CurrencyUnit(
        alpha_3="NGN",
        numeric="566",
        name="Naira",
    )
    NIO = CurrencyUnit(
        alpha_3="NIO",
        numeric="558",
        name="Cordoba Oro",
    )
    NOK = CurrencyUnit(
        alpha_3="NOK",
        numeric="578",
        name="Norwegian Krone",
    )
    NPR = CurrencyUnit(
        alpha_3="NPR",
        numeric="524",
        name="Nepalese Rupee",
    )
    NZD = CurrencyUnit(
        alpha_3="NZD",
        numeric="554",
        name="New Zealand Dollar",
    )
    OMR = CurrencyUnit(
        alpha_3="OMR",
        numeric="512",
        name="Rial Omani",
        digits=3,
    )
    PAB = CurrencyUnit(
        alpha_3="PAB",
        numeric="590",
        name="Balboa",
    )
    PEN = CurrencyUnit(
        alpha_3="PEN",
        numeric="604",
        name="Sol",
    )
    PGK = CurrencyUnit(
        alpha_3="PGK",
        numeric="598",
        name="Kina",
    )
    PHP = CurrencyUnit(
        alpha_3="PHP",
        numeric="608",
        name="Philippine Peso",
    )
    PKR = CurrencyUnit(
        alpha_3="PKR",
        numeric="586",
        name="Pakistan Rupee",
    )
    PLN = CurrencyUnit(
        alpha_3="PLN",
        numeric="985",
        name="Zloty",
    )
    PYG = CurrencyUnit(
        alpha_3="PYG",
        numeric="600",
        name="Guarani",
        digits=0,
    )
    QAR = CurrencyUnit(
        alpha_3="QAR",
        numeric="634",
        name="Qatari Rial",
    )
    RON = CurrencyUnit(
        alpha_3="RON",
        numeric="946",
        name="Romanian Leu",
    )
    RSD = CurrencyUnit(
        alpha_3="RSD",
        numeric="941",
        name="Serbian Dinar",
    )
    RUB = CurrencyUnit(
        alpha_3="RUB",
        numeric="643",
        name="Russian Ruble",
    )
    RWF = CurrencyUnit(
        alpha_3="RWF",
        numeric="646",
        name="Rwanda Franc",
        digits=0,
    )
    SAR = CurrencyUnit(
        alpha_3="SAR",
        numeric="682",
        name="Saudi Riyal",
    )
    SBD = CurrencyUnit(
        alpha_3="SBD",
        numeric="090",
        name="Solomon Islands Dollar",
    )
    SCR = CurrencyUnit(
        alpha_3="SCR",
        numeric="690",
        name="Seychelles Rupee",
    )
    SDG = CurrencyUnit(
        alpha_3="SDG",
        numeric="938",
        name="Sudanese Pound",
    )
    SEK = CurrencyUnit(
        alpha_3="SEK",
        numeric="752",
        name="Swedish Krona",
    )
    SGD = CurrencyUnit(
        alpha_3="SGD",
        numeric="702",
        name="Singapore Dollar",
    )
    SHP = CurrencyUnit(
        alpha_3="SHP",
        numeric="654",
        name="Saint Helena Pound",
    )
    SLE = CurrencyUnit(
        alpha_3="SLE",
        numeric="925",
        name="Leone",
    )
    SLL = CurrencyUnit(
        alpha_3="SLL",
        numeric="694",
        name="Leone",
    )
    SOS = CurrencyUnit(
        alpha_3="SOS",
        numeric="706",
        name="Somali Shilling",
    )
    SRD = CurrencyUnit(
        alpha_3="SRD",
        numeric="968",
        name="Surinam Dollar",
    )
    SSP = CurrencyUnit(
        alpha_3="SSP",
        numeric="728",
        name="South Sudanese Pound",
    )
    STN = CurrencyUnit(
        alpha_3="STN",
        numeric="930",
        name="Dobra",
    )
    SVC = CurrencyUnit(
        alpha_3="SVC",
        numeric="222",
        name="El Salvador Colon",
    )
    SYP = CurrencyUnit(
        alpha_3="SYP",
        numeric="760",
        name="Syrian Pound",
    )
    SZL = CurrencyUnit(
        alpha_3="SZL",
        numeric="748",
        name="Lilangeni",
    )
    THB = CurrencyUnit(
        alpha_3="THB",
        numeric="764",
        name="Baht",
    )
    TJS = CurrencyUnit(
        alpha_3="TJS",
        numeric="972",
        name="Somoni",
    )
    TMT = CurrencyUnit(
        alpha_3="TMT",
        numeric="934",
        name="Turkmenistan New Manat",
    )
    TND = CurrencyUnit(
        alpha_3="TND",
        numeric="788",
        name="Tunisian Dinar",
        digits=3,
    )
    TOP = CurrencyUnit(
        alpha_3="TOP",
        numeric="776",
        name="Pa’anga",  # noqa: RUF001
    )
    TRY = CurrencyUnit(
        alpha_3="TRY",
        numeric="949",
        name="Turkish Lira",
    )
    TTD = CurrencyUnit(
        alpha_3="TTD",
        numeric="780",
        name="Trinidad and Tobago Dollar",
    )
    TWD = CurrencyUnit(
        alpha_3="TWD",
        numeric="901",
        name="New Taiwan Dollar",
    )
    TZS = CurrencyUnit(
        alpha_3="TZS",
        numeric="834",
        name="Tanzanian Shilling",
    )
    UAH = CurrencyUnit(
        alpha_3="UAH",
        numeric="980",
        name="Hryvnia",
    )
    UGX = CurrencyUnit(
        alpha_3="UGX",
        numeric="800",
        name="Uganda Shilling",
        digits=0,
    )
    USD = CurrencyUnit(
        alpha_3="USD",
        numeric="840",
        name="US Dollar",
    )
    USN = CurrencyUnit(
        alpha_3="USN",
        numeric="997",
        name="US Dollar (Next day)",
    )
    UYI = CurrencyUnit(
        alpha_3="UYI",
        numeric="940",
        name="Uruguay Peso en Unidades Indexadas (UI)",
    )
    UYU = CurrencyUnit(
        alpha_3="UYU",
        numeric="858",
        name="Peso Uruguayo",
    )
    UYW = CurrencyUnit(
        alpha_3="UYW",
        numeric="927",
        name="Unidad Previsional",
    )
    UZS = CurrencyUnit(
        alpha_3="UZS",
        numeric="860",
        name="Uzbekistan Sum",
    )
    VED = CurrencyUnit(
        alpha_3="VED",
        numeric="926",
        name="Bolívar Soberano",
    )
    VES = CurrencyUnit(
        alpha_3="VES",
        numeric="928",
        name="Bolívar Soberano",
    )
    VND = CurrencyUnit(
        alpha_3="VND",
        numeric="704",
        name="Dong",
        digits=0,
    )
    VUV = CurrencyUnit(
        alpha_3="VUV",
        numeric="548",
        name="Vatu",
        digits=0,
    )
    WST = CurrencyUnit(
        alpha_3="WST",
        numeric="882",
        name="Tala",
    )
    XAF = CurrencyUnit(
        alpha_3="XAF",
        numeric="950",
        name="CFA Franc BEAC",
        digits=0,
    )
    XAG = CurrencyUnit(
        alpha_3="XAG",
        numeric="961",
        name="Silver",
    )
    XAU = CurrencyUnit(
        alpha_3="XAU",
        numeric="959",
        name="Gold",
    )
    XBA = CurrencyUnit(
        alpha_3="XBA",
        numeric="955",
        name="Bond Markets Unit European Composite Unit (EURCO)",
    )
    XBB = CurrencyUnit(
        alpha_3="XBB",
        numeric="956",
        name="Bond Markets Unit European Monetary Unit (E.M.U.-6)",
    )
    XBC = CurrencyUnit(
        alpha_3="XBC",
        numeric="957",
        name="Bond Markets Unit European Unit of Account 9 (E.U.A.-9)",
    )
    XBD = CurrencyUnit(
        alpha_3="XBD",
        numeric="958",
        name="Bond Markets Unit European Unit of Account 17 (E.U.A.-17)",
    )
    XCD = CurrencyUnit(
        alpha_3="XCD",
        numeric="951",
        name="East Caribbean Dollar",
    )
    XDR = CurrencyUnit(
        alpha_3="XDR",
        numeric="960",
        name="SDR (Special Drawing Right)",
    )
    XOF = CurrencyUnit(
        alpha_3="XOF",
        numeric="952",
        name="CFA Franc BCEAO",
        digits=0,
    )
    XPD = CurrencyUnit(
        alpha_3="XPD",
        numeric="964",
        name="Palladium",
    )
    XPF = CurrencyUnit(
        alpha_3="XPF",
        numeric="953",
        name="CFP Franc",
        digits=0,
    )
    XPT = CurrencyUnit(
        alpha_3="XPT",
        numeric="962",
        name="Platinum",
    )
    XSU = CurrencyUnit(
        alpha_3="XSU",
        numeric="994",
        name="Sucre",
    )
    XTS = CurrencyUnit(
        alpha_3="XTS",
        numeric="963",
        name="Codes specifically reserved for testing purposes",
    )
    XUA = CurrencyUnit(
        alpha_3="XUA",
        numeric="965",
        name="ADB Unit of Account",
    )
    XXX = CurrencyUnit(
        alpha_3="XXX",
        numeric="999",
        name="The codes assigned for transactions where no currency is involved",
    )
    YER = CurrencyUnit(
        alpha_3="YER",
        numeric="886",
        name="Yemeni Rial",
    )
    ZAR = CurrencyUnit(
        alpha_3="ZAR",
        numeric="710",
        name="Rand",
    )
    ZMW = CurrencyUnit(
        alpha_3="ZMW",
        numeric="967",
        name="Zambian Kwacha",
    )
    ZWL = CurrencyUnit(
        alpha_3="ZWL",
        numeric="932",
        name="Zimbabwe Dollar",
    )

    @property
    def unit(self) -> CurrencyUnit:
        """
        Returns:
            ``pycountries.currencies.CurrencyUnit``.
        """
        return self._value_

    @property
    def value(self) -> str:
        """
        Returns:
            ISO 4217 code.
        """
        return self.unit.alpha_3

    @property
    def alpha_3(self) -> str:
        """
        A three-letter alphabetic code.
        This alphabetic code is used internationally to represent currencies in financial transactions and data.

        Returns:
            ISO 4217 code.
        """
        return self.unit.alpha_3

    @property
    def numeric(self) -> str:
        """
        Numeric code. Preferred over alphabetic ones, such as in databases or systems where numeric identifiers
        are easier to work with.

        Returns:
            ISO 4217 numeric.
        """
        return self.unit.numeric

    @property
    def name(self) -> str:
        """
        The full currency name.

        Returns:
            ISO 4217 name.
        """
        return self.unit.name

    @property
    def digits(self) -> int:
        """
        Maximum currency digits.
        The maximum currency digits for many major currencies like the US Dollar (USD), Euro (EUR),
        and British Pound Sterling (GBP) is 2, meaning that values are typically rounded to two decimal places.
        However, there are exceptions, such as the Kuwaiti Dinar (KWD), which has a maximum currency digits of 3.

        Returns:
            ISO 4217 decimal.
        """
        return self.unit.digits

    @classmethod
    def _clean_decimal(cls, amount: Decimal, digits: int, missing_digits_number: int, /) -> Decimal:
        separator: str = ""
        if digits == 0:
            separator = "."
        if missing_digits_number == 0:
            return amount

        return Decimal(f'{amount!s}{separator}{missing_digits_number * "0"}')

    @singledispatchmethod
    def _get_exponent(self, exponent: str | int) -> int:
        raise NotImplementedError() from None

    @_get_exponent.register
    def _(self, exponent: str) -> int:
        raise ValueError() from None

    @_get_exponent.register
    def _(self, exponent: int) -> int:
        return abs(exponent)

    def _fix_missing_digits(self, amount: Decimal, exponent: int, /) -> Decimal:
        missing_digits_amount: int = self.digits - exponent
        return self._clean_decimal(amount, exponent, missing_digits_amount)

    def clean_amount(self, amount: Decimal, /, *, allow_zero: bool = True) -> Decimal:
        """Cleans the given ``amount`` based on the ``self.unit.digits`` decimal precision.

        Keep in mind ``amount`` must be with fixed point, otherwise, the behaviour unpredictable.
        Why we support only fixed points? Because pydantic by default uses this representation and for
        payments always better to use fixed points.

        >>> from decimal import Decimal
        >>> from pycountries.currencies import (
        >>>     AmountSpecialValuesNotAllowedError,
        >>>     NegativeAmountNotAllowedError,
        >>>     WrongAmountDigitsNumberError,
        >>>     WrongAmountTypeError,
        >>>     ZeroAmountNotAllowedError,
        >>> )
        >>>
        >>> correct_amount = Decimal("12")
        >>> Currency.BIF.clean_amount(correct_amount)  # BIF has 0 digits
        >>> Decimal("12")
        >>>
        >>> wrong_special_amount = Decimal("inf")
        >>> try:
        >>>     Currency.BIF.clean_amount(wrong_special_amount)
        >>> except AmountSpecialValuesNotAllowedError:
        >>>     print("Amount Special Values Not Allowed")
        >>>
        >>> negative_amount = Decimal("-20.22")
        >>> try:
        >>>     Currency.BIF.clean_amount(negative_amount)
        >>> except NegativeAmountNotAllowedError:
        >>>     print("Negative Amount Not Allowed")
        >>>
        >>> wrong_digits_amount = Decimal("12.3")
        >>> try:
        >>>     Currency.BIF.clean_amount(wrong_digits_amount)
        >>> except WrongAmountDigitsNumberError:
        >>>     print("Wrong Amount Digits Number")
        >>>
        >>> wrong_type_amount = 22
        >>> try:
        >>>     Currency.BIF.clean_amount(wrong_type_amount)
        >>> except WrongAmountTypeError:
        >>>     print("Wrong Amount Type")
        >>>
        >>> wrong_type_amount = Decimal("0.000")
        >>> try:
        >>>     Currency.BIF.clean_amount(wrong_type_amount)
        >>> except ZeroAmountNotAllowedError:
        >>>     print("Zero Amount Not Allowed")
        >>>
        >>> correct_amount_missing_digits = Decimal("12.3")
        >>> Currency.USD.clean_amount(correct_amount_missing_digits)  # USD has 2 digits
        >>> Decimal("12.30")

        Args:
            amount (decimal.Decimal): The amount to clean. Please pass only fixed point representation.x
            allow_zero (bool): If False only non-zero values are allowed.

        Returns:
            decimal.Decimal: The cleaned amount with the appropriate precision.

        Raises:
            pycountries.WrongAmountTypeError: If ``amount`` has not allowed type.
            pycountries.NegativeAmountNotAllowedError: If ``amount`` is negative.
            pycountries.ZeroAmountNotAllowedError: If ``amount`` is zero when ``allow_zero`` is False.
            pycountries.AmountSpecialValuesNotAllowedError: If ``amount`` is infinite or NaN.
            pycountries.WrongAmountDigitsNumberError: If ``amount`` has more digites than currency can have.
        """
        if not isinstance(amount, Decimal):
            raise WrongAmountTypeError() from None
        if amount.is_signed():
            raise NegativeAmountNotAllowedError() from None
        if not allow_zero and amount.is_zero():
            raise ZeroAmountNotAllowedError() from None
        try:
            exponent: int = self._get_exponent(amount.as_tuple().exponent)
        except ValueError:
            raise AmountSpecialValuesNotAllowedError() from None
        if exponent > self.digits:
            raise WrongAmountDigitsNumberError() from None
        else:
            amount = self._fix_missing_digits(amount, exponent)
        return amount

    @classmethod
    def zero_digits(cls) -> list[Currency]:
        """
        Returns:
            list[pycountries.currencies.Currency]: The list of currencies which have no digits.
        """
        return cls.zero_digits()

    @classmethod
    def two_digits(cls) -> list[Currency]:
        """
        Returns:
            list[pycountries.currencies.Currency]: The list of currencies which have maximum two digits.
        """
        return cls.two_digits()

    @classmethod
    def three_digits(cls) -> list[Currency]:
        """
        Returns:
            list[pycountries.currencies.Currency]: The list of currencies which have maximum three digits.
        """
        return cls.three_digits()

    def __str__(self) -> str:
        return self.value
