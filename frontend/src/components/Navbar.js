import React from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';

const Nav = styled.nav`
    background-color: #333;
    color: #fff;
    padding: 10px;
`;

const Ul = styled.ul`
    list-style-type: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: row;

    @media (max-width: 600px) {
        flex-direction: column;
        align-items: center;
    }
`;

const Li = styled.li`
    margin: 0 10px;

    @media (max-width: 600px) {
        margin: 10px 0;
    }
`;

const StyledLink = styled(Link)`
    color: #fff;
    text-decoration: none;
    padding: 5px 10px;
    border-radius: 5px;

    &:hover {
        background-color: #555;
        transition: background-color 0.3s ease-in-out;
    }
`;

const Navbar = () => {
    return (
        <Nav>
            <Ul>
                <Li><StyledLink to="/">Simulation</StyledLink></Li>
                <Li><StyledLink to="/history">Transaction History</StyledLink></Li>
            </Ul>
        </Nav>
    );
};

export default Navbar;
