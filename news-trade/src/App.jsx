import { useEffect, useState } from "react";

import { createClient } from "@supabase/supabase-js";
import Auth from './Auth';
import Avatar from "./Avatar";
import 'bootstrap/dist/css/bootstrap.min.css';

const supabase = createClient(
  "https://yfsyfoytsfpvnozqbnsm.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlmc3lmb3l0c2Zwdm5venFibnNtIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTY2Mzc0MTksImV4cCI6MjAxMjIxMzQxOX0.Q5Xbh8H4GFw-r3K7B3xLCFkcf7TUXPK3605SJpQLclA");


function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [profile, setProfile] = useState('');


  useEffect(() => {
    const authToken = localStorage.getItem('sb-yfsyfoytsfpvnozqbnsm-auth-token');

    if (authToken) {
      setIsAuthenticated(true)
    } else {
      setIsAuthenticated(false)
    }

  }, []);

  const handleChildValue = (value) => {
    setIsAuthenticated(value);
  };

  const handleProfile = (session) => {
    setProfile(session);
    setIsAuthenticated(true)
  }

  return (
    <>
      {isAuthenticated ? (
        <>

            <div className="App">
              <Avatar profile={ profile } supabaseClient={supabase}/>
            </div>
        </>
      ) : (
        <Auth handleChildValue={handleChildValue} handleProfile={handleProfile} />
      )}
    </>
  );
}

export default App;
