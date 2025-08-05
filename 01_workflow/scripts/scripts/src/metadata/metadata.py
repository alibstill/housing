from .metadata_class import Metadata

price_paid = Metadata(
    title="price_paid",
    creator="HM Land Registry",
    source="http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/",
    columns={
        "transaction_uid": {
            "type": "string",
            "description": "A reference number which is generated automatically recording each published sale. The number is unique and will change each time a sale is recorded.",
        },
        "price": {
            "type": "int",
            "description": "Sale price stated on the transfer deed.",
        },
        "date_of_transfer": {
            "type": "string",
            "description": "YYYY-MM-DD. Date when the sale was completed, as stated on the transfer deed.",
        },
        "postcode": {
            "type": "string",
            "description": "This is the postcode used at the time of the original transaction. Note that postcodes can be reallocated and these changes are not reflected in the Price Paid Dataset.",
        },
        "property_type": {
            "type": "string",
            "description": "D = Detached, S = Semi-Detached, T = Terraced, F = Flats/Maisonettes, O = Other Note that: we only record the above categories to describe property type, we do not separately identify bungalows. End-of-terrace properties are included in the Terraced category above. ‘Other’ is only valid where the transaction relates to a property type that is not covered by existing values, for example where a property comprises more than one large parcel of land.",
        },
        "is_new_build": {
            "type": "string",
            "description": "Indicates the age of the property and applies to all price paid transactions, residential and non-residential: Y = a newly built property, N = an established residential building",
        },
        "tenure_duration": {
            "type": "string",
            "description": "Relates to the tenure: F = Freehold, L= Leasehold etc. Note that HM Land Registry does not record leases of 7 years or less in the Price Paid Dataset.",
        },
        "paon": {
            "type": "string",
            "description": "Primary Addressable Object Name. Typically the house number or name.",
        },
        "saon": {
            "type": "string",
            "description": "Secondary Addressable Object Name. Where a property has been divided into separate units (for example, flats), the PAON (above) will identify the building and a SAON will be specified that identifies the separate unit/flat.",
        },
        "street": {"type": "string", "description": "The street name of the property"},
        "locality": {
            "type": "string",
            "description": "An additional description of address location if there is more than one paon/street name in the same town/city",
        },
        "town_city": {"type": "string", "description": "The town or city of the property"},
        "district": {
            "type": "string",
            "description": "An additional description of address location. A subdivision of a county",
        },
        "county": {
            "type": "string",
            "description": "An additional description of address location. Towns and cities are in counties.",
        },
        "transaction_type": {
            "type": "string",
            "description": "Indicates the type of Price Paid transaction. A = Standard Price Paid entry, includes single residential property sold for value. B = Additional Price Paid entry including transfers under a power of sale/repossessions, buy-to-lets (where they can be identified by a Mortgage), transfers to non-private individuals and sales where the property type is classed as ‘Other’. Note that category B does not separately identify the transaction types stated. HM Land Registry has been collecting information on Category A transactions from January 1995. Category B transactions were identified from October 2013.",
        },
        "record_status": {
            "type": "string",
            "description": "monthly file only (yearly files are all 'A'). Indicates additions, changes and deletions to the records.A = Addition, C = Change, D = Delete. Note that where a transaction changes category type due to misallocation (as above) it will be deleted from the original category type and added to the correct category with a new transaction unique identifier. The single large file and yearly files have amendments and/or deletions applied to the data, ensuring the data is complete, up to date and accurate. Subsequent monthly files may contain amendments if a record is added, changed or deleted. If an amendment is made a status marker will appear at the end of the record to indicate the type of change. You will need to consider this change if you compare month files.",
        },
    },
)
