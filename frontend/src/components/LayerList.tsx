import React, {FunctionComponent} from "react";
import {CollapsibleList, ListItem, ListItemText, SimpleListItem} from '@rmwc/list'
import 'rmwc/dist/styles'
import autoBind from 'react-autobind';
import {Configuration, DefaultApiFactory} from '../client'

interface Layer {
    id: number
    label: string
    active: boolean
}

type LayerGroupState = {}

type LayerGroupProps = {
    label: string
    icon: string
    layers: Layer[]
}

export class LayerGroup extends React.Component<LayerGroupProps, LayerGroupState> {
    api: ReturnType<typeof DefaultApiFactory>
    apiConfig: Configuration

    constructor(props: LayerGroupProps) {
        super(props)
        this.state = {}
        autoBind(this);
        this.apiConfig = new Configuration({basePath: "http://localhost:8000/"})
        this.api = DefaultApiFactory(this.apiConfig)
        console.log(this.api.getLayersLayersGet())
    }

    render() {
        const listItems = this.props.layers.map((layer) => <LayerListItem key={layer.id} label={layer.label}
                                                                          active={layer.active}/>);
        return (
            <CollapsibleList
                handle={<SimpleListItem text={this.props.label} graphic={this.props.icon} metaIcon="chevron_right"/>}>
                {listItems}
            </CollapsibleList>
        )
    }
}

export const LayerGroup2: FunctionComponent<LayerGroupProps> = ({label, icon, layers}) => {
    const listItems = layers.map((layer) => <LayerListItem key={layer.id} label={layer.label}
                                                           active={layer.active}/>);
    return (
        <CollapsibleList
            handle={<SimpleListItem text={label} graphic={icon} metaIcon="chevron_right"/>}>
            {listItems}
        </CollapsibleList>)
}

type LayerListItemProps = {
    label: string
    active: boolean
}

// we can use children even though we haven't defined them in our CardProps
export const LayerListItem: FunctionComponent<LayerListItemProps> = ({label, active}) =>
    <ListItem>
        <ListItemText>
            {label}
        </ListItemText>
    </ListItem>