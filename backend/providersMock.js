export const DEMO_LOC = { lat: 40.7506, lng: -73.9972 }; // near 10001

export const PROVIDERS = [
  { id:'p1', name:'Ana Builds', skill_tags:['furniture_assembly'], rate_hour:45, avg_rating:4.9,
    lat:40.754, lng:-73.99, service_radius_km:20, reliability:0.9,
    stats:{ furniture_assembly:{ jobs_done:72, completion_rate:0.98 } } },
  { id:'p2', name:'Handy Mike', skill_tags:['handyman','furniture_assembly'], rate_hour:40, avg_rating:4.7,
    lat:40.742, lng:-73.99, service_radius_km:15, reliability:0.85,
    stats:{ furniture_assembly:{ jobs_done:35, completion_rate:0.96 }, handyman:{ jobs_done:58, completion_rate:0.95 } } },
  { id:'p3', name:'Swift Movers', skill_tags:['moving_help'], rate_hour:50, avg_rating:4.6,
    lat:40.745, lng:-74.004, service_radius_km:25, reliability:0.88,
    stats:{ moving_help:{ jobs_done:120, completion_rate:0.97 } } },
  { id:'p4', name:'Clean Junk Co', skill_tags:['junk_removal'], rate_hour:55, avg_rating:4.8,
    lat:40.761, lng:-73.985, service_radius_km:30, reliability:0.92,
    stats:{ junk_removal:{ jobs_done:210, completion_rate:0.99 } } },
  { id:'p5', name:'Metro Pest', skill_tags:['pest_control'], rate_hour:85, avg_rating:4.9,
    lat:40.748, lng:-73.99, service_radius_km:25, reliability:0.93,
    stats:{ pest_control:{ jobs_done:340, completion_rate:0.98 } }, regulatory:['licensed_pest_control'] },
];
