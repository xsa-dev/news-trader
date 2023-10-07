import React, { useState } from 'react';

import { createClient } from '@supabase/supabase-js'
const supabase = createClient(
    "https://yfsyfoytsfpvnozqbnsm.supabase.co",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlmc3lmb3l0c2Zwdm5venFibnNtIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTY2Mzc0MTksImV4cCI6MjAxMjIxMzQxOX0.Q5Xbh8H4GFw-r3K7B3xLCFkcf7TUXPK3605SJpQLclA");
  import { Form, Button } from 'react-bootstrap';


const Auth = (props) => {
    const [login, setLogin] = useState('');
    const [password, setPassword] = useState('');
    const [isBot, setIsBot] = useState(true);

    const handleLogin = async () => {
        // Replace this with your actual authentication logic
        if (login === '' && password === '') {
            alert('Имя пользователя или логин не могут быть пустым!');
        } else if (login === 'admin' && password === 'admin') {
            props.handleChildValue(true); // Corrected this line
            console.log('Logged in successfully');
        } else {
            // authorization with supabase login+password
            const { data, error } = await supabase.auth.signInWithPassword({
                email: login,
                password: password,
            });
            if (error) {
                alert(error);
            }

            if (data) {
                console.log('Logged in with Supabase');
                props.handleChildValue(true); 
                props.handleProfile(data);
            }

            console.log(data);            
        }
    };



    return (
        <>
            <div>
                <div className="center">
                    <Form >
                        <Form.Group controlId="formBasicLogin">
                            <Form.Control
                                type="text"
                                placeholder="Введите логин:"
                                value={login}
                                onChange={(e) => setLogin(e.target.value)}
                            />
                        </Form.Group>

                        <Form.Group controlId="formBasicPassword">
                            <Form.Control
                                type="password"
                                placeholder="Введите пароль:"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </Form.Group>

                        <Form.Group controlId='notRobot'>
                            <Form.Check
                                type="checkbox"
                                label="save" // Label for the checkbox
                                checked={isBot} // Use the state value to control the checkbox
                                onChange={(e) => setIsBot(e.target.checked)} // Update the state when the checkbox changes
                            />
                        </Form.Group>

                        <Button variant="primary" onClick={handleLogin}>
                            Login
                        </Button>
                    </Form>

                </div>
            </div>
        </>
    )
};

export default Auth;