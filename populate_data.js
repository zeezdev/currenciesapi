var currencies = [
    {"name": "Bitcoin", "code": "BTC"},
    {"name": "United States dollar", "code": "USD"},
    {"name": "Ethereum", "code": "ETH"},
    {"name": "Monero", "code": "XMR"},
    {"name": "Waves", "code": "WAVES"},
    {"name": "Zcash", "code": "ZEC"},
    {"name": "Ripple", "code": "XRP"},
    {"name": "Dash", "code": "DASH"},
    {"name": "Ethereum Classic", "code": "ETC"},
    {"name": "Bitcoin Cash", "code": "BCH"},
    {"name": "Litecoin", "code": "LTC"},
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
{ currency: "XRP", value: 2.3409 },
{ currency: "DASH", value: 1057.0 },
{ currency: "ETC", value: 34.5 },
{ currency: "BCH", value: 2445.0 },
{ currency: "LTC", value: 230.0 },
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
        var doc = Object.assign({}, data[i]);
        doc.ts = currDate;
        var v =  doc.value;
        var pct = (v/100) * (Math.random() * 10.0);
        doc.value = v + (pct * (Math.random() ? 1 : -1));
        print(doc.value);
        db.rates_history.insert(doc);
    }
    currDate.setMinutes(currDate.getMinutes() + 10);
}