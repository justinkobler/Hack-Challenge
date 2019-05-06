//
//  Networking.swift
//  ezscore
//
//  Created by Karen Papazian on 5/5/19.
//  Copyright © 2019 Karen Papazian. All rights reserved.
//

import Foundation
import Alamofire


struct Teams: Codable {
    var id: Int
    var name: String
}

struct Score: Codable {
    var score: String
}

class Network {
    
    static func getTeams(cb: @escaping (([Teams]) -> Void)) {
        Alamofire.request("backend_url/teams").responseData { data in
            let teams = try! JSONDecoder().decode([Teams].self, from: data.data!)
            cb(teams)
        }
    }
    
    static func getScore(teamID: Int, cb: @escaping ((Score) -> Void)) {
        Alamofire.request("backend_url/score\(teamID)").responseData { data in
            let score = try! JSONDecoder().decode(Score.self, from: data.data!)
            cb(score)
        }
    }
}
