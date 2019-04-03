var currencies = [
    {"name": "Bitcoin", "code": "BTC"},
    {"name": "United States dollar", "code": "USD"},
    {"name": "Ethereum", "code": "ETH"},
    {"name": "Monero", "code": "XMR"},
    {"name": "Waves", "code": "WAVES"},
    {"name": "Zcash", "code": "ZEC"},
];

for (var i=0; i < currencies.length; i++) {
    db.currencies.updateOne({code: currencies[i].code}, {"$set": {name: currencies[i].name}}, {upsert: true});
};



var data = [
{ currency: "BTC", value: 4736.0 },
{ currency: "ETH", value: 156.0 },
{ currency: "XMR", value: 363.0 },
{ currency: "WAVES", value: 12.61 },
{ currency: "ZEC", value: 587.0 },
];

for (var i=0; i < data.length; i++) {
    db.rates.updateOne({currency: data[i].currency}, {"$set": {value: data[i].value}}, {upsert: true});
};

// Populate historical data for one year (2018) with a step 10 min
db.rates_history.deleteMany({});
var currDate = new Date('2018-01-01T00:00:00Z');
var endDate = new Date('2019-01-01T00:00:00Z');
while (currDate < endDate) {
    for (var i=0; i < data.length; i++) {
        var doc = data[i];
        doc.ts = currDate;
        db.rates_history.insert(doc);
    }
    currDate.setMinutes(currDate.getMinutes() + 10);
}