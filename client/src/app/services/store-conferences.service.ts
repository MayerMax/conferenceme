import { Injectable } from '@angular/core';
import {ReplaySubject} from "rxjs/ReplaySubject";
import {Conference} from "../constructor/models/Conference";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs/Observable";

@Injectable()
export class StoreConferencesService {
  ConferencesSubject$ = new ReplaySubject<Conference[]>(null);
  private BaseUrl = 'http://localhost:8080';
  constructor(private  http: HttpClient) { }
public gerNewConference(): Observable<Conference>{
    let url =`${this.BaseUrl}/new_conference`;
  return this.http.get<Conference>(url).map(
    conference => {
      console.log(conference)
      // let {id,name,topics,begin_date,end_date,sections,lectures,speakers,logo}= conference;
      return conference;
    } );
}
  public getData(){
    let url = `${this.BaseUrl}/all_conferences`;
    return this.http.get<Conference[]>(url).map(
      conference => {
        if (conference != null) {
         conference.map(conference=>{
           conference.begin_date = Conference.parseDate(conference.begin_date);
           conference.end_date = Conference.parseDate(conference.end_date);
           return conference
         } );
        }
        return conference;
      }
    ).subscribe(this.ConferencesSubject$);
  }

}
