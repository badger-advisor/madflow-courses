const axios = require('axios').default;

const config = {
  url     : 'https://public.enroll.wisc.edu/api/search/v1',
  method  : 'POST',
  data    : JSON.stringify({
    selectedTerm : '1232',
    queryString  : '*',
    filters      : [
      { term: { 'subject.subjectCode': '266' } },
      {
        has_child : {
          type  : 'enrollmentPackage',
          query : { match: { published: true } }
        }
      }
    ],
    page         : 1,
    pageSize     : 90,
    sortOrder    : 'SCORE'
  }),
  headers : {
    'Content-Type' : 'application/json'
  }
};

const getCourses = async () => {
  try {
    const res = await axios(config);
    return res.data.hits;
  } catch (e) {
    console.log(e);
  }
};

const main = async () => {
  const courses = await getCourses();
  console.log(courses);
};

main();
