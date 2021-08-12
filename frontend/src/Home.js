import React from 'react';

const todoItems = [
  {
    id: 1,
    title: "Nature walk in the park",
    description: "Visit the park with my friends",
    completed: true
  },

  {
    id: 2,
    title: "Visit",
    description: "Got to my aunt's place",
    completed: true
  },
];

function Home() {
  return (
      <main className="content">
          <div className="row">
              <div className="col-md-6 col-sm-10 mx-auto p-0">
                  <div className="card p-3">
                      <ul className="list-group list-group-flush">
                          {todoItems.map(item => (
                              <div>
                                  <h1>{item.title}</h1>
                                  <span>{item.description}</span>
                              </div>
                          ))}
                      </ul>
                  </div>
              </div>
          </div>
      </main>
  );
}

export default Home;
