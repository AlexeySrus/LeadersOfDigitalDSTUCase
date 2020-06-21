import React, {Component} from 'react';
import './App.css';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import ListItem from 'material-ui/List/ListItem';
import List from 'material-ui/List/List';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import Paper from 'material-ui/Paper';
import Polarity from "./components/Polarity";

const style = {
    marginLeft: 150
};

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            'curriculum_relevance_score': '',
            'scientific_activity': '',
            'avg_region_salary_increase': '',
            'top_5_job_fields': '',
            polarity: undefined
        };
    };

    analyzeSentence() {
        fetch('http://0.0.0.0:5000/api/compute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(
                {
                            'program_name': this.textField1.getValue(),
                            'maker': this.textField2.getValue(),
                            'maker_science_degree': this.textField3.getValue(),
                            'competencies': this.textField4.getValue(),
                            'university': this.textField5.getValue()
                        }
                )
        })
            .then(response => response.json())
            .then(data => this.setState(data));
    }

    onEnterPress = e => {
        if (e.key === 'Enter') {
            this.analyzeSentence();
        }
    };

    render() {
        const polarityComponent = this.state.polarity !== undefined ?
            <Polarity sentence={this.state.sentence} polarity={this.state.polarity}/> :
            null;

        return (
            <MuiThemeProvider>
                    <List className="centerize">
                        <Paper zDepth={1} className="content">
                    <div className="content">
                        <h2>Введите данные обучающей программы</h2>
                        <div className="content">
                        <TextField ref={ref => this.textField1 = ref} onKeyUp={this.onEnterPress.bind(this)}
                                   hintText="Введите название обучающей программы"/>
                        </div>
                        <div className="content">
                        <TextField ref={ref => this.textField2 = ref} onKeyUp={this.onEnterPress.bind(this)}
                                   hintText="Введите составителя обучающей программы в формате `Фамилия И.О.`"/>
                        </div>
                        <div className="content">
                        <TextField ref={ref => this.textField3 = ref} onKeyUp={this.onEnterPress.bind(this)}
                                   hintText="Введите ученую степень составителя (одно из: `нет`, `кандидат наук`, `доктор наук`)"/>
                        </div>
                        <div className="content">
                        <TextField ref={ref => this.textField4 = ref} onKeyUp={this.onEnterPress.bind(this)}
                                   hintText="Введите список компетенций с разделениеч через симол ;"/>
                        </div>
                        <div className="content">
                        <TextField ref={ref => this.textField5 = ref} onKeyUp={this.onEnterPress.bind(this)}
                                   hintText="Введите название университета (один из `DSTU`, 'SFEDU')"/>
                        </div>
                    </div>
                    <RaisedButton  label="Send" style={style} onClick={this.analyzeSentence.bind(this)}/>
                    {polarityComponent}
                    {/*<div className="content">*/}
                    {/*    <h1>Result: {JSON.stringify(this.state,null, 4)}</h1>*/}
                        <h3>Степень качества образовательной программы: {this.state['curriculum_relevance_score']}</h3>
                        <h3>Степень научной активности: {this.state['scientific_activity']}</h3>
                        <h3>Отношение зарплаты к средней по региону: {this.state['avg_region_salary_increase']}</h3>
                        <h3>Топ 5 специализаций для выпускника: <br></br>{JSON.stringify(this.state['top_5_job_fields'],null, 4)}</h3>
                        {/*<TextField ref={ref => this.textField5 = ref} onKeyUp={this.onEnterPress.bind(this)}*/}
                        {/*           hintText={JSON.stringify(this.state,null, 4)}/>*/}
                    {/*</div>*/}
                        </Paper>
                    </List>
            </MuiThemeProvider>
        );
    }
}

export default App;