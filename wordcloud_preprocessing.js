// https://github.com/amueller/word_cloud

const fs = require('fs');
const {parse} = require('csv-parse');

const write_distinct = fs.createWriteStream('./data/generated/wordcloud_raw_distinct.txt');

fs.createReadStream('./data/generated/debotted_combined_distinct.csv')
  .pipe(parse({
      delimiter: ',',
      columns: true
  }))
  .on('data', function (row) {
      write_distinct.write(row.content);
  });

const write = fs.createWriteStream('./data/generated/wordcloud_raw.txt');

fs.createReadStream('./data/generated/debotted_combined.csv')
  .pipe(parse({
      delimiter: ',',
      columns: true
  }))
  .on('data', function (row) {
      write.write(row.content);
  });
