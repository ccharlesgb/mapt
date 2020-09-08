import React from "react";
import {Drawer, DrawerContent, DrawerHeader, DrawerTitle} from '@rmwc/drawer';
import {CollapsibleList, List, ListDivider, ListItem, ListItemGraphic, ListItemText, SimpleListItem} from '@rmwc/list'
import 'rmwc/dist/styles'
import autoBind from 'react-autobind';
import './Sidebar.css'
import {ListOnActionEventT} from "@rmwc/list/dist/list";

type SidebarState = {}

type SidebarProps = {
    onUploadClicked: (evt: ListOnActionEventT) => void;
}

class Sidebar extends React.Component<SidebarProps, SidebarState> {
    constructor(props: SidebarProps) {
        super(props)
        this.state = {}
        autoBind(this);
    }

    render() {
        return (
            <React.Fragment>
                <Drawer>
                    <DrawerHeader>
                        <DrawerTitle>Datasets</DrawerTitle>
                    </DrawerHeader>
                    <DrawerContent>
                        <List onAction={this.props.onUploadClicked}>
                            <ListItem>
                                <ListItemGraphic icon="add" />
                                <ListItemText>
                                    Upload Data
                                </ListItemText>
                            </ListItem>
                        </List>
                        <ListDivider/>
                        <CollapsibleList
                            handle={<SimpleListItem text="Favourites" graphic="favorite" metaIcon="chevron_right"/>}>
                            <SimpleListItem text="First"/>
                            <SimpleListItem text="Second"/>
                        </CollapsibleList>
                        <CollapsibleList
                            handle={<SimpleListItem text="Recent" graphic="watch_later" metaIcon="chevron_right"/>}>
                            <SimpleListItem text="First"/>
                            <SimpleListItem text="Second"/>
                        </CollapsibleList>
                        <ListDivider/>
                        <CollapsibleList
                            handle={<SimpleListItem text="Boundaries" graphic="subject" metaIcon="chevron_right"/>}>
                            <SimpleListItem text="First"/>
                            <SimpleListItem text="Second"/>
                        </CollapsibleList>
                        <CollapsibleList
                            handle={<SimpleListItem text="Census" graphic="subject" metaIcon="chevron_right"/>}>
                            <SimpleListItem text="First"/>
                            <SimpleListItem text="Second"/>
                        </CollapsibleList>
                        <CollapsibleList
                            handle={<SimpleListItem text="Transport" graphic="subject" metaIcon="chevron_right"/>}>
                            <SimpleListItem text="First"/>
                            <SimpleListItem text="Second"/>
                        </CollapsibleList>
                    </DrawerContent>
                </Drawer>
            </React.Fragment>
        );
    }
}

export default Sidebar