import { IoBanSharp } from "react-icons/io5";
import { AiFillCloseCircle } from "react-icons/ai";
import { MdDelete } from "react-icons/md";
import {useState} from "react";
import SidebarMenu from 'react-bootstrap-sidebar-menu';
import AddWordModal from "./AddWordModal";

function BlacklistSideBar(props) {
    return (
        <>
            <SidebarMenu style={{backgroundColor: "white", height: 30*props.words.length + 150}}>
                <SidebarMenu.Header>
                    <SidebarMenu.Brand>
                        {"Blacklist"}
                    </SidebarMenu.Brand>
                </SidebarMenu.Header>
                <SidebarMenu.Body>
                    <SidebarMenu.Nav>
                        <SidebarMenu.Nav.Link>
                            <ul>
                                {props.words.map((item, index) => {
                                    return (
                                        <li key={index}>
                                            <SidebarMenu.Nav.Icon>
                                                <MdDelete onClick={() => props.removeWord(item, index)}/>
                                            </SidebarMenu.Nav.Icon>
                                            {item.word}
                                        </li>
                                    )
                                })}
                            </ul>
                        </SidebarMenu.Nav.Link>
                    </SidebarMenu.Nav>
                </SidebarMenu.Body>
                <br/>
                <AddWordModal handleAdd={props.handleAdd}/>
            </SidebarMenu>
        </>
    )
} export default BlacklistSideBar;