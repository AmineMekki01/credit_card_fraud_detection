import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styled from 'styled-components';

const Container = styled.div`
    max-width: 800px;
    margin: 2rem auto;
    padding: 2rem;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
`;

const Title = styled.h1`
    font-size: 2.5rem;
    color: #333;
    margin-bottom: 1.5rem;
    text-align: center;
`;

const List = styled.ul`
    list-style: none;
    padding: 0;
    margin: 0;
`;

const ListItem = styled.li`
    padding: 1rem;
    border-bottom: 1px solid #ddd;
    display: flex;
    justify-content: space-between;
    &:last-child {
        border-bottom: none;
    }
`;

const TransactionID = styled.span`
    font-weight: bold;
    color: #555;
`;

const Status = styled.span`
    color: ${props => props.status === 'Fraud' ? 'red' : 'green'};
`;

const History = () => {
    const [transactions, setTransactions] = useState([]);

    useEffect(() => {
        const fetchTransactions = async () => {
            try {
                const response = await axios.get('http://localhost:8000/transactions');
                setTransactions(response.data);
            } catch (error) {
                console.error("Error fetching transactions:", error);
            }
        };

        fetchTransactions();
    }, []);

    return (
        <Container>
            <Title>Transaction History</Title>
            <List>
                {transactions.map((transaction) => (
                    <ListItem key={transaction.transaction_id}>
                        <TransactionID>ID: {transaction.transaction_id}</TransactionID>
                        <Status status={transaction.status}>Prediction: {transaction.status}</Status>
                    </ListItem>
                ))}
            </List>
        </Container>
    );
};

export default History;
