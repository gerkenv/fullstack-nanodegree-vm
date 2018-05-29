'use strict'

import {simpleFetch} from 'helperfunctions'

let main = () => {
  simpleFetch('GET', 'localhost:5000/readHello');
};

main();