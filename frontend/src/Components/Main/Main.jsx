import React, { Component } from 'react';
import './Main.css';
import Tweets from '../TweetsBoard/Tweets';
import Loader from 'react-loader-spinner';
import SmallBoard from '../SmallBoard/SmallBoard';
import "react-loader-spinner/dist/loader/css/CradleLoader.css";

export default class Menu extends Component {
	constructor(props) {
		super(props);
		this.state = {
			overAllData: [{ label: "Total Cases", value: 0, className: "text-primary", showValue: true },
			{ label: "New Cases", value: 0, className: "text-warning", showValue: true },
			{ label: "Deceased Cases", value: 0, className: "text-danger", showValue: true }],
			showSmallBoard: true,
			isLoggedIn: sessionStorage.getItem('isLoggedIn')
		}
		this.handleClick = this.handleClick.bind(this);
	};
	componentDidUpdate(prevProps, prevState) {
		if (prevProps.overAllData !== this.props.overAllData) {
			//Perform some operation here
			const { total_cases, total_deaths, new_cases } = this.props.overAllData;
			this.setState({
				overAllData: [{ label: "Total Cases", value: total_cases, className: "text-primary", showValue: true },
				{ label: "New Cases", value: new_cases, className: "text-warning", showValue: true },
				{ label: "Deceased Cases", value: total_deaths, className: "text-danger", showValue: true },
				]
			})
		}
	};

	toggleSideBar = () => {
		this.props.toggleSideBar();
	}

	logout = () => {
		this.props.onLogout();
		this.setState({
			isLoggedIn:false
		})
	}
	
	showLogin=()=>{
		this.props.showLogin();
	}

	setIsLoggedIn=()=>{
		this.props.setIsLoggedIn();
		this.setState({
			isLoggedIn:sessionStorage.getItem('isLoggedIn')
		})
	}

	handleClick(label) {
		var selectedValue = this.state.overAllData.find((item) => item.label === label);
		selectedValue.showValue = !selectedValue.showValue;
		this.setState({overAllData: [...this.state.overAllData]});
	}

	render() {
		return (
			<div className="main">
				<nav class="navbar navbar-dark bg-dark">
					<button class="navbar-toggler" type="button" onClick={this.toggleSideBar}
						data-toggle="collapse" data-target="#navbarToggleExternalContent"
						aria-controls="navbarToggleExternalContent" aria-expanded="false" aria-label="Toggle navigation">
						<span class="navbar-toggler-icon"></span>
					</button>
					{this.state.isLoggedIn && <button className="btn btn-light logout" type="submit" disabled={this.props.spinner} onClick={this.state.isLoggedIn ? this.logout : this.showLogin}>
					{this.state.isLoggedIn ? 'Logout' : 'Login' }
              		</button>}
				</nav>
				<main className="content">
					<div className="container-fluid">
						<div class="main_header">
							<h1 class="header-title">
								COVID-19 Twitter Data
						</h1>
						</div>
						<div class="row row_gap">
							<div class="col-xl-6 col-xxl-5 d-flex">
								<div class="w-100">
									<div class="row" id='chat-body'>
										{this.state.overAllData.map((stats, idx) => (
											<SmallBoard
												key={idx}
												handleClick={this.handleClick}
												value={stats.value}
												label={stats.label}
												showValue={stats.showValue}
												className={stats.className}
											/>
										))}
									</div>
								</div>
							</div>
						</div>
						<div className="row description">
							Aggregated dashboard for seeing twitter data for helping everyone fighting COVID-19. The counts shown are sourced from
    						ECDC and was updated on {this.props.createdDate && new Intl.DateTimeFormat("en-GB", {
							year: "numeric",
							month: "short",
							day: "2-digit"
						}).format(new Date(this.props.createdDate))}.
						</div>
						{this.props.spinner && <div class="row">
							<div className='spinnerClass'>
								<Loader type="CradleLoader" color="#2BAD60" height='100' width='100' />
							</div>
						</div>
						}
						<div className='row'>
							<Tweets setIsLoggedIn={this.setIsLoggedIn} isLoggedIn={this.state.isLoggedIn}/>
						</div>
					</div>
				</main>
			</div>
		)
	}
}

