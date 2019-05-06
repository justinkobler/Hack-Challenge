//
//  ChooseTeamViewController.swift
//  ezscore
//
//  Created by Karen Papazian on 4/24/19.
//  Copyright © 2019 Karen Papazian. All rights reserved.
//

import UIKit

protocol TeamSelectedDelegate {
    func teamWasSelected(team: String, isRival: Bool)
}

class ChooseTeamViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
    
    var tableView: UITableView!
    
    var delegate: TeamSelectedDelegate?
    
    var teams = [
        "San Diego Padres",
        "Aneheim Angels",
        "Los Angeles Dodgers",
        "Oakland Athletics",
        "San Francisco Giants",
        "Texas Rangers",
        "New York Yankees",
        "New York Mets",
        "Boston Red Sox",
        "Arizona Diamondbacks",
        "Miami Marlins",
        "Baltimore Orioles",
        "Tampa Bay Rays",
        "Toronto Blue Jays",
        "Houston Astros",
        "Colorado Rockies",
        "Cincinatti Reds",
        "Chicago White Sox",
        "Detroit Tigers",
        "Philadelphia Phillies",
        "Washington Nationals",
        "Atlanta Braves",
        "Milwaukee Brewers",
        "Kansas City Royals",
        "Chicago Cubs",
        "Seattle Mariners",
        "Cleveland Indians",
        "Minnesota Twins",
        "Pittsburgh Pirates",
        "St. Louis Cardinals",
        ]
    
    var isRival = false
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        view.backgroundColor = .white
        
        // Do any additional setup after loading the view.
        
        tableView = UITableView(frame: .zero, style: .grouped)
        tableView.backgroundColor = .white
        tableView.dataSource = self
        tableView.delegate = self
        tableView.translatesAutoresizingMaskIntoConstraints = false
        tableView.register(TeamTableViewCell.self, forCellReuseIdentifier: "team-cell")
        view.addSubview(tableView)
        
        tableView.leadingAnchor.constraint(equalTo: view.leadingAnchor).isActive = true
        tableView.trailingAnchor.constraint(equalTo: view.trailingAnchor).isActive = true
        tableView.topAnchor.constraint(equalTo: view.topAnchor).isActive = true
        tableView.bottomAnchor.constraint(equalTo: view.bottomAnchor).isActive = true
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return teams.count
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        print("CHOSE TEAM: \(teams[indexPath.row])")
        delegate?.teamWasSelected(team: teams[indexPath.row], isRival: isRival)
        dismiss(animated: true, completion: nil)
    }
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, titleForHeaderInSection section: Int) -> String? {
        return "Choose Team"
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "team-cell", for: indexPath) as! TeamTableViewCell
        cell.teamNameLabel.text = teams[indexPath.row]
        return cell
    }
    
}

