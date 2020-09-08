import React from "react";
import {TopAppBar, TopAppBarFixedAdjust, TopAppBarRow, TopAppBarSection, TopAppBarTitle} from '@rmwc/top-app-bar'
import 'rmwc/dist/styles'
import autoBind from 'react-autobind';

type TopbarState = {}

type TopbarProps = {}

class Topbar extends React.Component<TopbarProps, TopbarState> {
    constructor(props: TopbarProps) {
        super(props)
        this.state = {}
        autoBind(this);
    }

    render() {
        return (
            <React.Fragment>
                <TopAppBar fixed>
                    <TopAppBarRow>
                        <TopAppBarSection>
                            <TopAppBarTitle>Mapt</TopAppBarTitle>
                        </TopAppBarSection>
                    </TopAppBarRow>
                </TopAppBar>
                <TopAppBarFixedAdjust/>
            </React.Fragment>

        );
    }
}

export default Topbar