//
//  TeamTableViewCell.swift
//  ezscore
//
//  Created by Karen Papazian on 4/24/19.
//  Copyright © 2019 Karen Papazian. All rights reserved.
//

import UIKit

class TeamTableViewCell: UITableViewCell {
    
    var teamNameLabel: UILabel!
    
    override init(style: UITableViewCell.CellStyle, reuseIdentifier: String?) {
        super.init(style: style, reuseIdentifier: reuseIdentifier)
        teamNameLabel = UILabel()
        teamNameLabel.translatesAutoresizingMaskIntoConstraints = false
        contentView.addSubview(teamNameLabel)
        
        teamNameLabel.leadingAnchor.constraint(equalTo: contentView.leadingAnchor).isActive = true
        teamNameLabel.topAnchor.constraint(equalTo: contentView.topAnchor).isActive = true
        teamNameLabel.bottomAnchor.constraint(equalTo: contentView.bottomAnchor).isActive = true
        teamNameLabel.trailingAnchor.constraint(equalTo: contentView.trailingAnchor).isActive = true
    }
    
    required init?(coder aDecoder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
