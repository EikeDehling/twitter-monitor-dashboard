import ReactDOM  from 'react-dom';
import React from 'react';
import rd3 from 'rd3';
import $ from 'jquery';
import {TagCloud, DefaultRenderer} from "react-tagcloud";

const LineChart = rd3.LineChart;
const AreaChart = rd3.AreaChart;

var ChartThing = React.createClass({
  getInitialState() {
    return {
      data: null,
      type: 'volume',
      keywords: 'amsterdam'
    };
  },

  dataReceived(data) {
    if (this.state.type === 'volume' || this.state.type === 'reach') {
      for (var i = 0; i < data[0].values.length; ++i) {
        data[0].values[i].x = new Date(data[0].values[i].x);
      }
    }

    this.setState({data: data});
  },

  handleKeywordChange(e) {
    this.setState({keywords: e.target.value});
    this.getData()
  },

  handleTypeChange(e) {
    this.setState({type: e.target.value});
    this.getData()
  },

  getData() {
    this.setState({data: null});
    $.ajax({
      url: "/data/" + this.state.type,
      data: { keywords: this.state.keywords }
    }).done(this.dataReceived);
  },

  componentDidMount() {
    this.getData();
  },

  handleSubmit(e) {
    e.preventDefault();
    this.getData();
  },

  renderChart() {
    if (!this.state.data) {
      return null;
    }

    switch (this.state.type) {
      case 'tagcloud':
        return (<TagCloud
                  minSize={12}
                  maxSize={35}
                  style={{width: 300}}
                  tags={this.state.data} />
                );

      case 'reach':
      case 'volume':
        return (
          <LineChart
            data={this.state.data}
            width={600} height={400}
            title="Volume data"
            yAxisLabel="Volume"
            xAxisLabel="Time"
            xAxisTickInterval={{unit: 'hour', interval: 1}} />
        );

      case 'postings':
        return (
            <table>
              <tr>
                <th>Author</th>
                <th>Date</th>
                <th>Text</th>
              </tr>
              {this.state.data.map((x, i) =>
                <tr key={i + 1}>
                  <td>{x['author']}</td>
                  <td>{x['created_at']}</td>
                  <td>{x['text']}</td>
                </tr>
              )}
            </table>
        );

      case 'clusters':
        return (
            <table>
              <tr>
                <th>Cluster name</th>
                <th># docs</th>
                <th>Keywords</th>
              </tr>
              {this.state.data.map((x, i) =>
                <tr key={i + 1}>
                  <td>{x['label']}</td>
                  <td>{x['documents']}</td>
                  <td>
                      {x['keywords'].map((y, j) =>
                         <p>{y['key']}</p>
                      )}
                  </td>
                </tr>
              )}
            </table>
        );

      default:
        return (<table>
                  <tr>
                    <th>{this.state.type}</th>
                    <th>Count</th>
                  </tr>
                  {this.state.data.map((x, i) =>
                    <tr key={i + 1}>
                      <td>{x['key']}</td>
                      <td>{x['doc_count']}</td>
                    </tr>
                  )}
                </table>);
    }

  },

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          Keywords: <input name="keywords" type="text" value={this.state.keywords} onChange={this.handleKeywordChange} />
          Type:
          <select name="type" value={this.state.type} onChange={this.handleTypeChange}>
            <option value="volume">Volume</option>
            <option value="reach">Reach</option>
            <option value="postings">Postings</option>
            <option value="tagcloud">Tagcloud</option>
            <option value="clusters">Clusters</option>
            <option value="author">Authors</option>
            <option value="hashtags">Hashtags</option>
            <option value="urls">Links</option>
            <option value="mentions">Mentioned users</option>
          </select>
          <input type="submit" value="Submit" />
        </form>

        {this.renderChart()}
      </div>
    );
  }
});

ReactDOM.render(<ChartThing />, document.getElementById('react-chart'));