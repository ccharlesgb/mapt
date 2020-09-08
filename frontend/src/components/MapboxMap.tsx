import React from "react";
import {Button} from '@rmwc/button';
import 'rmwc/dist/styles'
import mapboxgl from 'mapbox-gl';
import './MapboxMap.css'

const token = process.env["REACT_APP_MAPBOX_ACCESS_TOKEN"]
if (!token) {
    throw new Error("Environment variable MAPBOX_ACCESS_TOKEN is not defined")
}
mapboxgl.accessToken = token

type MapboxMapState = { lng: number, lat: number, zoom: number }

type MapboxMapProps = {}

class MapboxMap extends React.Component<MapboxMapProps, MapboxMapState> {
    mapContainer: HTMLDivElement | null | undefined

    constructor(props: MapboxMapProps) {
        super(props)
        this.state = {lng: 0.0, lat: 55.0, zoom: 5}
    }

    componentDidMount() {
        if (this.mapContainer) {
            const map = new mapboxgl.Map({
                container: this.mapContainer,
                style: 'mapbox://styles/mapbox/streets-v11',
                center: [this.state.lng, this.state.lat],
                zoom: this.state.zoom
            });
        }
    }

    render() {
        return (
            <React.Fragment>
                <div ref={x => this.mapContainer = x}/>
            </React.Fragment>
        )
    }
}

export default MapboxMap