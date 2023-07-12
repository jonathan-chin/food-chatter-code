const {Parser} = require('json2csv'); 
const fs = require('fs');

const parser = new Parser({
    fields: ['cluster_name', 'cluster_number', 'docs', 'keywords']
});

const categories = [
    'access_justice',
    'community',
    'food_insecurity',
    'food_quality',
    'prices',
    'snap_wic_school',
    'stores_brands',
    'struggle'
];

const process = (category) => {
    const raw = fs.readFileSync(`./data/generated/report_no_rts_${category}.txt`, 'utf8');
    let payload = [];
    // get documents per cluster
    const docs_regex = /Number of documents per topic: (\[[ \d\n]+\])/g;
    const docs_count = docs_regex.exec(raw)[1].replace(/[\[\]]/g, '').trim().replace(/\s+/g, ',').split(',');
    
    // first get all clusters
    const clusters = raw.match(/Cluster \d+ : \[.*\]/g).slice(0, 10);
    for(const cluster of clusters){
	// get cluster number
	const cluster_number_regex = /Cluster (\d+)/g;
	const cluster_number = parseInt(cluster_number_regex.exec(cluster)[1]);
	const cluster_docs_count = docs_count[cluster_number];

	// extract keywords
	const keywords_regex = /\('(\w+)', \d*\)/g;
	let last_match;
	let keywords = [];
	while(last_match = keywords_regex.exec(cluster)){
	    keywords.push(last_match[1]);
	}
	payload.push({
	    cluster_name: category,
	    cluster_number,
	    docs: parseInt(cluster_docs_count),
	    keywords: keywords.join(' ')
	});
    }
    const csv = parser.parse(payload);
    fs.writeFileSync(`./data/generated/cluster_keywords_no_rts_${category}.csv`, csv);
}

for(const category of categories){
    process(category);
}
