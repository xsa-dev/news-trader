import { useEffect, useState } from 'react'
import { Form, Button } from 'react-bootstrap';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export default function Avatar({ profile, supabase }) {
    const [connected, setConnected] = useState(false);

    console.log(profile, supabase)

    const handleConnect = () => {
        setConnected(true)
    }

    const handleLogout = () => {

            localStorage.removeItem('sb-yfsyfoytsfpvnozqbnsm-auth-token');
            window.location.href = '/';
        
    }

    const handleLogin = () => {
        alert('login!')
    }



    return (
        <Container className='center'>
            {
                connected ? (
                    <Row>
                        <Col>
                            <Form >
                                <Form.Group controlId="formTradeSystemKey">
                                    <Form.Control
                                        type="text"
                                        placeholder="binance key"
                                        // value={login}
                                        onChange={(e) => setLogin(e.target.value)}
                                    />
                                </Form.Group>

                                <Form.Group controlId="formTradeSystemSecret">
                                    <Form.Control
                                        type="password"
                                        placeholder="binance secret:"
                                        // value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                    />
                                </Form.Group>

                                <Form.Group controlId='trade'>
                                    <Form.Check
                                        type="checkbox"
                                        label="Trade" // Label for the checkbox
                                        // checked={use} // Use the state value to control the checkbox
                                        onChange={(e) => setIsBot(e.target.checked)} // Update the state when the checkbox changes
                                    />
                                </Form.Group>
                                <div>
                                    <Button variant="warning" onClick={handleLogin}>
                                        Update
                                    </Button>
                                    <Button variant="secondary" onClick={handleLogout}>
                                        Exit
                                    </Button>
                                </div>
                            </Form>
                        </Col>
                    </Row>
                ) : (
                    <div>
                        <Row>
                            <Col>
                                <Button variant="primary" onClick={handleConnect}>
                                    Connect Wallet
                                </Button>
                            </Col>
                        </Row>
                        <Row><Col>                
                        <Button variant="secondary" onClick={handleLogout}>
                            Logout System
                        </Button>
                        </Col>
                        </Row>
                    </div>
                )

            }

        </Container>
    )
}