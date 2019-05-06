//
//  TeamScoreViewController.swift
//  ezscore
//
//  Created by Karen Papazian on 5/5/19.
//  Copyright © 2019 Karen Papazian. All rights reserved.
//

import UIKit

class TeamScoreViewController: UIViewController {
    
    var scoreLabel: UILabel!

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .white

        title = "Team Score"
        
        scoreLabel = UILabel()
        scoreLabel.text = "5 - 0"
        scoreLabel.font = UIFont.boldSystemFont(ofSize: 24)
        scoreLabel.translatesAutoresizingMaskIntoConstraints = false
        scoreLabel.textAlignment = .center
        view.addSubview(scoreLabel)
        
        scoreLabel.leadingAnchor.constraint(equalTo: view.leadingAnchor).isActive = true
        scoreLabel.trailingAnchor.constraint(equalTo: view.trailingAnchor).isActive = true
        scoreLabel.topAnchor.constraint(equalTo: view.topAnchor, constant: 100).isActive = true
        scoreLabel.heightAnchor.constraint(equalToConstant: scoreLabel.intrinsicContentSize.height).isActive = true
    }
    
}
